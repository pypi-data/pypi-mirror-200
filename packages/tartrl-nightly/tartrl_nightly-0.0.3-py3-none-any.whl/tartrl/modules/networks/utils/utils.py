import math
from typing import Dict, Union, Tuple
import dataclasses
import itertools
from collections.abc import Mapping

import numpy as np
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
import time

@dataclasses.dataclass
class ActionIndex:
    start: int
    end: int


def get_action_indices(act_dims):
    curr_action_index = 0
    action_indices = []
    for dim in act_dims:
        action_indices.append(ActionIndex(curr_action_index, curr_action_index + dim))
        curr_action_index += dim
    return action_indices

def mlp(sizes, activation=nn.ReLU, layernorm=True):
    layers = []
    for j in range(len(sizes) - 1):
        layers += [nn.Linear(sizes[j], sizes[j + 1]), activation()]
        if layernorm:
            layers += [nn.LayerNorm([sizes[j + 1]])]
    return nn.Sequential(*layers)

def make_models_for_obs(obs_dim: Dict[str, Union[int, Tuple]], hidden_dim: int, activation,
                        cnn_layers: Dict[str, Tuple]):
    obs_embd_dict = nn.ModuleDict()
    for k, v in obs_dim.items():
        if isinstance(v, int):
            obs_embd_dict.update({
                k: nn.Sequential(nn.LayerNorm([v]),
                                 mlp([v, hidden_dim], activation=activation, layernorm=True))
            })
        else:
            raise NotImplementedError()
    return obs_embd_dict


class RunningMeanStd(nn.Module):

    def __init__(self, input_shape, beta=0.999, epsilon=1e-5):
        super().__init__()
        self.__beta = beta
        self.__eps = epsilon
        self.__input_shape = input_shape

        self.__mean = nn.Parameter(torch.zeros(input_shape), requires_grad=False)
        self.__mean_sq = nn.Parameter(torch.zeros(input_shape), requires_grad=False)
        self.__debiasing_term = nn.Parameter(torch.zeros(1), requires_grad=False)

        self.reset_parameters()

    def reset_parameters(self):
        self.__mean.zero_()
        self.__mean_sq.zero_()
        self.__debiasing_term.zero_()

    def forward(self, *args, **kwargs):
        # we don't implement the forward function because its meaning
        # is somewhat ambiguous
        raise NotImplementedError

    def __check(self, x):
        assert isinstance(x, torch.Tensor)
        trailing_shape = x.shape[-len(self.__input_shape):]
        assert trailing_shape == self.__input_shape, (
            'Trailing shape of input tensor'
            f'{x.shape} does not equal to configured input shape {self.__input_shape}')

    @torch.no_grad()
    def update(self, x):
        self.__check(x)
        norm_dims = tuple(range(len(x.shape) - len(self.__input_shape)))

        batch_mean = x.mean(dim=norm_dims)
        batch_sq_mean = x.square().mean(dim=norm_dims)
        if dist.is_initialized():
            world_size = dist.get_world_size()
            dist.all_reduce(batch_mean)
            dist.all_reduce(batch_sq_mean)
            batch_mean /= world_size
            batch_sq_mean /= world_size

        self.__mean.mul_(self.__beta).add_(batch_mean * (1.0 - self.__beta))
        self.__mean_sq.mul_(self.__beta).add_(batch_sq_mean * (1.0 - self.__beta))
        self.__debiasing_term.mul_(self.__beta).add_(1.0 * (1.0 - self.__beta))

    @torch.no_grad()
    def mean_std(self):
        debiased_mean = self.__mean / self.__debiasing_term.clamp(min=self.__eps)
        debiased_mean_sq = self.__mean_sq / self.__debiasing_term.clamp(min=self.__eps)
        debiased_var = (debiased_mean_sq - debiased_mean**2).clamp(min=1e-2)
        return debiased_mean, debiased_var.sqrt()

    @torch.no_grad()
    def normalize(self, x):
        self.__check(x)
        mean, std = self.mean_std()
        return (x - mean) / std

    @torch.no_grad()
    def denormalize(self, x):
        self.__check(x)
        mean, std = self.mean_std()
        return x * std + mean


def mlp(sizes, activation=nn.ReLU, layernorm=True):
    layers = []
    for j in range(len(sizes) - 1):
        layers += [nn.Linear(sizes[j], sizes[j + 1]), activation()]
        if layernorm:
            layers += [nn.LayerNorm([sizes[j + 1]])]
    return nn.Sequential(*layers)

class AutoResetRNN(nn.Module):

    def __init__(self, input_dim, output_dim, num_layers=1, batch_first=False, rnn_type='gru'):
        super().__init__()
        self.__type = rnn_type
        # print(batch_first)
        # import pdb;pdb.set_trace()
        if self.__type == 'gru':
            self.__net = nn.GRU(input_dim, output_dim, num_layers=num_layers, batch_first=batch_first)
        elif self.__type == 'lstm':
            self.__net = nn.LSTM(input_dim, output_dim, num_layers=num_layers, batch_first=batch_first)
        else:
            raise NotImplementedError(f'RNN type {self.__type} has not been implemented.')
        self._recurrent_N = num_layers

    def __forward(self, x, h):
        if self.__type == 'lstm':
            h = torch.split(h, h.shape[-1] // 2, dim=-1)
            h = (h[0].contiguous(), h[1].contiguous())
        x_, h_ = self.__net(x, h)
        if self.__type == 'lstm':
            h_ = torch.cat(h_, -1)
        return x_, h_

    def forward(self, x, hxs, masks=None):

        if x.size(0) == hxs.size(0):
            x, hxs = self.__forward(x.unsqueeze(0), (hxs * masks.repeat(1, self._recurrent_N).unsqueeze(-1)).transpose(0, 1).contiguous())
            #x= self.gru(x.unsqueeze(0))
            x = x.squeeze(0)
            # hxs = hxs.transpose(0, 1)
        else:
            # x is a (T, N, -1) tensor that has been flatten to (T * N, -1)
            N = hxs.size(0)
            T = int(x.size(0) / N)

            # unflatten
            x = x.view(T, N, x.size(1))

            # Same deal with masks
            masks = masks.view(T, N)

            # Let's figure out which steps in the sequence have a zero for any agent
            # We will always assume t=0 has a zero in it as that makes the logic cleaner
            has_zeros = ((masks[1:] == 0.0)
                         .any(dim=-1)
                         .nonzero()
                         .squeeze()
                         .cpu())

            # +1 to correct the masks[1:]
            if has_zeros.dim() == 0:
                # Deal with scalar
                has_zeros = [has_zeros.item() + 1]
            else:
                has_zeros = (has_zeros + 1).numpy().tolist()

            # add t=0 and t=T to the list
            has_zeros = [0] + has_zeros + [T]

            hxs = hxs.transpose(0, 1)

            outputs = []
            for i in range(len(has_zeros) - 1):
                # We can now process steps that don't have any zeros in masks together!
                # This is much faster
                start_idx = has_zeros[i]
                end_idx = has_zeros[i + 1]
                temp = (hxs * masks[start_idx].view(1, -1, 1).repeat(self._recurrent_N, 1, 1)).contiguous()
                rnn_scores, hxs = self.__forward(x[start_idx:end_idx], temp)
                outputs.append(rnn_scores)

            # assert len(outputs) == T
            # x is a (T, N, -1) tensor
            x = torch.cat(outputs, dim=0)

            # flatten
            x = x.reshape(T * N, -1)
            # hxs = hxs.transpose(0, 1)
        return x, hxs
        # if on_reset is None:
        #     x_, h_ = self.__forward(x, h)
        # else:
        #     outputs = []
        #     for t in range(on_reset.shape[0]):
        #         x_, h = self.__forward(x[t:t + 1], (h * (1 - on_reset[t:t + 1])).contiguous())
        #         outputs.append(x_)
        #     x_ = torch.cat(outputs, 0)
        #     h_ = h
        # return x_, h_


class RecurrentBackbone(nn.Module):

    @property
    def feature_dim(self):
        return self.__feature_dim

    def __init__(
            self,
            obs_dim: int,
            dense_layers: int,
            hidden_dim: int,
            rnn_type: str,
            num_rnn_layers: int,
            dense_layer_gain: float = math.sqrt(2),
            activation='relu',
            layernorm=True,
            batch_first=True
    ):
        super(RecurrentBackbone, self).__init__()

        if activation == 'relu':
            act_fn = nn.ReLU
        elif activation == 'tanh':
            act_fn = nn.Tanh
        elif activation == 'elu':
            act_fn = nn.ELU
        elif activation == 'gelu':
            act_fn = nn.GELU
        else:
            raise NotImplementedError(f"Activation function {activation} not implemented.")

        self.__feature_dim = hidden_dim
        self.__rnn_type = rnn_type
        self.fc = mlp([obs_dim, *([hidden_dim] * dense_layers)], act_fn, layernorm=layernorm)
        for k, p in self.fc.named_parameters():
            if 'weight' in k and len(p.data.shape) >= 2:
                # filter out layer norm weights
                nn.init.orthogonal_(p.data, gain=dense_layer_gain)
            if 'bias' in k:
                nn.init.zeros_(p.data)

        self.num_rnn_layers = num_rnn_layers
        if self.num_rnn_layers:
            self.rnn = AutoResetRNN(hidden_dim,
                                            hidden_dim,
                                            num_layers=num_rnn_layers,
                                            rnn_type=self.__rnn_type,batch_first=batch_first)
            self.rnn_norm = nn.LayerNorm([hidden_dim])
            for k, p in self.rnn.named_parameters():
                if 'weight' in k and len(p.data.shape) >= 2:
                    # filter out layer norm weights
                    nn.init.orthogonal_(p.data)
                if 'bias' in k:
                    nn.init.zeros_(p.data)

    def forward(self, obs, hx, on_reset=None):
        features = self.fc(obs)
        if self.num_rnn_layers > 0:
            features, hx = self.rnn(features, hx, on_reset)
            features = self.rnn_norm(features)
        return features, hx




def _is_dataclass_instance(obj):
    return dataclasses.is_dataclass(obj) and not isinstance(obj, type)


def is_namedarray_instance(obj):
    flag = _is_dataclass_instance(obj) and hasattr(obj, '_fields')
    flag = flag and hasattr(obj, 'items') and issubclass(type(obj), Mapping)
    return flag and not isinstance(obj, type)


def __namedarray_op(op):

    def fn(self, value):
        if not (_is_dataclass_instance(value) and  # Check for matching structure.
                getattr(value, "_fields", None) == self._fields):
            if not _is_dataclass_instance(value):
                value = tuple(None if s is None else value for s in self)
            else:
                raise ValueError('namedarray - set an item with a different data structure')
        try:
            xs = []
            for j, (s, v) in enumerate(zip(self, value)):
                if s is not None and v is not None:
                    exec(f"xs.append(s {op} v)")
        except (ValueError, IndexError, TypeError) as e:
            raise Exception(f"{type(e).__name__} occured in {self.__class__.__name__}"
                            " at field "
                            f"'{self._fields[j]}': {e}") from e
        return type(self)(*xs)

    return fn


def __namedarray_iop(iop):

    def fn(self, value):
        if not (_is_dataclass_instance(value) and  # Check for matching structure.
                getattr(value, "_fields", None) == self._fields):
            if not _is_dataclass_instance(value):
                value = {k: None if s is None else value for k, s in self.items()}
            else:
                raise ValueError('namedarray - set an item with a different data structure')
        try:
            for j, (k, v) in enumerate(zip(self.keys(), value.values())):
                if self[k] is not None and v is not None:
                    exec(f"self[k] {iop} v")
        except (ValueError, IndexError, TypeError) as e:
            raise Exception(f"{type(e).__name__} occured in {self.__class__.__name__}"
                            " at field "
                            f"'{self._fields[j]}': {e}") from e
        return self

    return fn


def namedarray(cls, *args, **kwargs):
    data_cls = dataclasses.dataclass(cls, *args, **kwargs)
    typename = data_cls.__class__.__name__

    def __iter__(self):

        def gen():
            for k in self.__dataclass_fields__.keys():
                yield getattr(self, k)

        return gen()

    def __getitem__(self, loc):
        if isinstance(loc, str):
            # str indexing like in dict
            return getattr(self, loc)
        else:
            try:
                return type(self)(*(None if s is None else s[loc] for s in self))
            except IndexError as e:
                for j, s in enumerate(self):
                    if s is None:
                        continue
                    try:
                        _ = s[loc]
                    except IndexError:
                        raise Exception(f"Occured in {self.__class__} at field "
                                        f"'{self._fields[j]}'.") from e

    def __setitem__(self, loc, value):
        if isinstance(loc, str):
            setattr(self, loc, value)
        else:
            if not (_is_dataclass_instance(value) and  # Check for matching structure.
                    getattr(value, "_fields", None) == self._fields):
                if not _is_dataclass_instance(value):
                    # Repeat value for each but respect any None.
                    value = tuple(None if s is None else value for s in self)
                else:
                    raise ValueError('namedarray - set an item with a different data structure')
            try:
                for j, (s, v) in enumerate(zip(self, value)):
                    if s is not None and v is not None:
                        s[loc] = v
            except (ValueError, IndexError, TypeError) as e:
                raise Exception(f"{type(e).__name__} occured in {self.__class__.__name__}"
                                " at field "
                                f"'{self._fields[j]}': {e}") from e

    def __contains__(self, key):
        return key in self._fields

    def values(self):
        for v in self:
            yield v

    def keys(self):
        for k in self._fields:
            yield k

    def items(self):
        for k, v in zip(self._fields, self):
            yield k, v

    def to_dict(self):
        result = {}
        for k, v in self.items():
            if is_namedarray_instance(v):
                result[k] = v.to_dict()
            elif v is None:
                result[k] = None
            else:
                result[k] = v
        return result

    @property
    def shape(self):
        return recursive_apply(self, lambda x: x.shape).to_dict()

    def size(self):
        return self.shape

    methods = [__getitem__, __setitem__, __iter__, __contains__, values, keys, items]

    for method in methods:
        method.__qualname__ = f'{typename}.{method.__name__}'

    ops = {
        '__add__': __namedarray_op('+'),
        '__sub__': __namedarray_op('-'),
        '__mul__': __namedarray_op('*'),
        '__truediv__': __namedarray_op('/')
    }
    iops = {
        '__iadd__': __namedarray_iop('+='),
        '__isub__': __namedarray_iop('-='),
        '__imul__': __namedarray_iop('*='),
        '__itruediv__': __namedarray_iop('/=')
    }
    for name, op in itertools.chain(ops.items(), iops.items()):
        op.__qualname__ = f'{typename}.{name}'

    arg_list = repr(list(data_cls.__dataclass_fields__.keys())).replace("'", "")[1:-1]
    class_namespace = {
        '__doc__': f'{typename}({arg_list})',
        '__slots__': (),
        '__iter__': __iter__,
        '_fields': list(data_cls.__dataclass_fields__.keys()),
        '__getitem__': __getitem__,
        '__setitem__': __setitem__,
        '__contains__': __contains__,
        'items': items,
        'keys': keys,
        'values': values,
        'to_dict': to_dict,
        'shape': shape,
        'size': size,
    }
    class_namespace = {**class_namespace, **ops, **iops}
    for k, v in class_namespace.items():
        setattr(data_cls, k, v)

    Mapping.register(data_cls)
    return data_cls


def array_like(x, value=0):
    if is_namedarray_instance(x):
        return type(x)(*[array_like(xx, value) for xx in x])
    else:
        if isinstance(x, np.ndarray):
            data = np.zeros_like(x)
        else:
            assert isinstance(x, torch.Tensor), ('Currently, namedarray only supports'
                                                 f' torch.Tensor and numpy.array (input is {type(x)})')
            data = torch.zeros_like(x)
        if value != 0:
            data[:] = value
        return data


def __array_filter_none(xs):
    is_not_nones = [x is not None for x in xs]
    if all(is_not_nones) or all(x is None for x in xs):
        return
    else:
        example_x = xs[is_not_nones.index(True)]
        for i, x in enumerate(xs):
            xs[i] = array_like(example_x) if x is None else x


def recursive_aggregate(xs, aggregate_fn):
    __array_filter_none(xs)
    assert all([type(x) == type(xs[0]) for x in xs]), ([type(x) for x in xs], xs)

    if is_namedarray_instance(xs[0]):
        return type(xs[0])(*[recursive_aggregate([x[k] for x in xs], aggregate_fn) for k in xs[0].keys()])
    elif xs[0] is None:
        return None
    else:
        return aggregate_fn(xs)


def recursive_apply(x, fn):
    if is_namedarray_instance(x):
        return type(x)(*[recursive_apply(v, fn) for v in x.values()])
    elif x is None:
        return None
    else:
        return fn(x)

class Action:
    pass

@namedarray
class DiscreteAction(Action):
    x: np.ndarray

    def __eq__(self, other):
        assert isinstance(other, DiscreteAction), \
            "Cannot compare DiscreteAction to object of class{}".format(other.__class__.__name__)
        return self.key == other.key

    def __hash__(self):
        return hash(self.x.item())

    @property
    def key(self):
        return self.x.item()

class PopArtValueHead(nn.Module):

    def __init__(self, input_dim, critic_dim, beta=0.999, epsilon=1e-5, burn_in_updates=torch.inf):
        super().__init__()
        self.__rms = RunningMeanStd((critic_dim,), beta, epsilon)

        self.__weight = nn.Parameter(torch.zeros(critic_dim, input_dim))
        nn.init.orthogonal_(self.__weight)
        self.__bias = nn.Parameter(torch.zeros(critic_dim))

        self.__burn_in_updates = burn_in_updates
        self.__update_cnt = 0

    def forward(self, feature):
        return F.linear(feature, self.__weight, self.__bias)

    @torch.no_grad()
    def update(self, x):
        old_mean, old_std = self.__rms.mean_std()
        self.__rms.update(x)
        new_mean, new_std = self.__rms.mean_std()
        self.__update_cnt += 1

        if self.__update_cnt > self.__burn_in_updates:
            self.__weight.data[:] = self.__weight * (old_std / new_std).unsqueeze(-1)
            self.__bias.data[:] = (old_std * self.__bias + old_mean - new_mean) / new_std

    @torch.no_grad()
    def normalize(self, x):
        return self.__rms.normalize(x)

    @torch.no_grad()
    def denormalize(self, x):
        return self.__rms.denormalize(x)
