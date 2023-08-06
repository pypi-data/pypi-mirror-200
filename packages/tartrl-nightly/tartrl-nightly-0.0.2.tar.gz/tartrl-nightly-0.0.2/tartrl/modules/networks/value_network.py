#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2021 The TARTRL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""""""

import torch
import torch.nn as nn

from tartrl.modules.networks.utils.util import init
from tartrl.modules.networks.utils.mlp import MLPBase, MLPLayer
from tartrl.modules.networks.utils.rnn import RNNLayer
from tartrl.modules.networks.utils.popart import PopArt
from tartrl.modules.networks.utils.mix import MIXBase
from tartrl.modules.networks.utils.cnn import CNNBase
from tartrl.modules.networks.utils.FcEncoder import FcEncoder
from tartrl.modules.networks.base_value_network import BaseValueNetwork

from tartrl.buffers.utils.util import get_shape_from_obs_space
from .utils.utils import make_models_for_obs, RecurrentBackbone, PopArtValueHead, recursive_apply
from tartrl.utils.util import check_v2 as check


class InputEncoder(nn.Module):
    def __init__(self):
        super(InputEncoder, self).__init__()
        fc_layer_num = 2
        fc_output_num = 64

        self.ball_owner_input_num = 35
        self.left_input_num = 88
        self.right_input_num = 88
        self.match_state_input_num = 9

        self.ball_owner_encoder = FcEncoder(fc_layer_num, self.ball_owner_input_num, fc_output_num)
        self.left_encoder = FcEncoder(fc_layer_num, self.left_input_num, fc_output_num)
        self.right_encoder = FcEncoder(fc_layer_num, self.right_input_num, fc_output_num)
        self.match_state_encoder = FcEncoder(fc_layer_num, self.match_state_input_num, self.match_state_input_num)

    def forward(self, x):
        ball_owner_vec = x[:, :self.ball_owner_input_num]
        left_vec = x[:, self.ball_owner_input_num: self.ball_owner_input_num + self.left_input_num]
        right_vec = x[:,
                    self.ball_owner_input_num + self.left_input_num:  self.ball_owner_input_num + self.left_input_num + self.right_input_num]
        match_state_vec = x[:, self.ball_owner_input_num + self.left_input_num + self.right_input_num:]

        ball_owner_output = self.ball_owner_encoder(ball_owner_vec)
        left_output = self.left_encoder(left_vec)
        right_output = self.right_encoder(right_vec)
        match_state_output = self.match_state_encoder(match_state_vec)

        return torch.cat([
            ball_owner_output,
            left_output,
            right_output,
            match_state_output
        ], 1)


class NewValueNetwork(BaseValueNetwork):
    def __init__(self, args, share_obs_space, device=torch.device("cpu")):
        super(NewValueNetwork, self).__init__(args, device)
        self.hidden_size = args.hidden_size
        self.tpdv = dict(dtype=torch.float32, device=device)

        input_embedding_size = 64 * 3 + 9
        self.input_encoder = InputEncoder()
        self.base = FcEncoder(3, input_embedding_size, self.hidden_size)
        self.rnn = RNNLayer(self.hidden_size, self.hidden_size, args.recurrent_N, args.use_orthogonal,
                            rnn_type=args.rnn_type)
        self.v_out = nn.Linear(self.hidden_size, 1)

        self.to(device)

    def forward(self, share_obs, rnn_states, masks):
        share_obs = check(share_obs).to(**self.tpdv)
        rnn_states = check(rnn_states).to(**self.tpdv)
        masks = check(masks).to(**self.tpdv)

        critic_features = self.input_encoder(share_obs)
        critic_features = self.base(critic_features)

        critic_features, rnn_states = self.rnn(critic_features, rnn_states, masks)
        values = self.v_out(critic_features)
        return values, rnn_states


class ValueNetwork(BaseValueNetwork):
    def __init__(self, args, input_space, action_space=None, use_half=False, device=torch.device("cpu")):
        super(ValueNetwork, self).__init__(args, device)

        self.hidden_size = args.hidden_size
        self._use_orthogonal = args.use_orthogonal
        self._activation_id = args.activation_id
        self._use_naive_recurrent_policy = args.use_naive_recurrent_policy
        self._use_recurrent_policy = args.use_recurrent_policy
        self._use_influence_policy = args.use_influence_policy
        self._use_popart = args.use_popart
        self._influence_layer_N = args.influence_layer_N
        self._recurrent_N = args.recurrent_N
        self.tpdv = dict(dtype=torch.float32, device=device)

        init_method = [nn.init.xavier_uniform_, nn.init.orthogonal_][self._use_orthogonal]

        share_obs_shape = get_shape_from_obs_space(input_space)

        if 'Dict' in share_obs_shape.__class__.__name__:
            self._mixed_obs = True
            self.base = MIXBase(args, share_obs_shape, cnn_layers_params=args.cnn_layers_params)
        else:
            self._mixed_obs = False
            self.base = CNNBase(args, share_obs_shape) if len(share_obs_shape) == 3 else MLPBase(args, share_obs_shape,
                                                                                                 use_attn_internal=True,
                                                                                                 use_cat_self=args.use_cat_self)

        input_size = self.base.output_size

        if self._use_naive_recurrent_policy or self._use_recurrent_policy:
            self.rnn = RNNLayer(input_size, self.hidden_size, self._recurrent_N, self._use_orthogonal,
                                rnn_type=args.rnn_type)
            input_size = self.hidden_size

        if self._use_influence_policy:
            self.mlp = MLPLayer(share_obs_shape[0], self.hidden_size,
                                self._influence_layer_N, self._use_orthogonal, self._activation_id)
            input_size += self.hidden_size

        def init_(m):
            return init(m, init_method, lambda x: nn.init.constant_(x, 0))

        if self._use_popart:
            self.v_out = init_(PopArt(input_size, 1, device=device))
        else:
            self.v_out = init_(nn.Linear(input_size, 1))

        self.to(device)

    def forward(self, share_obs, rnn_states, masks):
        if self._mixed_obs:
            for key in share_obs.keys():
                share_obs[key] = check(share_obs[key]).to(**self.tpdv)
        else:
            share_obs = check(share_obs).to(**self.tpdv)
        rnn_states = check(rnn_states).to(**self.tpdv)
        masks = check(masks).to(**self.tpdv)

        critic_features = self.base(share_obs)

        if self._use_naive_recurrent_policy or self._use_recurrent_policy:
            critic_features, rnn_states = self.rnn(critic_features, rnn_states, masks)

        if self._use_influence_policy:
            mlp_share_obs = self.mlp(share_obs)
            critic_features = torch.cat([critic_features, mlp_share_obs], dim=1)

        values = self.v_out(critic_features)

        return values, rnn_states


class XZLValueNetwork(BaseValueNetwork):
    def __init__(self, args, share_obs_space, device=torch.device("cpu")):
        super(XZLValueNetwork, self).__init__(args, device)
        self.tpdv = dict(dtype=torch.float32, device=device)
        share_obs_shape = get_shape_from_obs_space(share_obs_space)
        obs_dim = share_obs_shape[0]
        hidden_dim = args.hidden_size
        cnn_layers = None
        activation = ['tanh', 'relu', 'leaky_relu', 'leaky_relu'][args.activation_id]
        dense_layers = args.layer_N
        num_rnn_layers = args.rnn_num
        rnn_type = args.rnn_type
        layernorm = True

        if activation == 'relu':
            self.activation = nn.ReLU
        elif activation == 'tanh':
            self.activation = nn.Tanh
        else:
            raise NotImplementedError(f"Activation function {activation} not implemented.")

        if isinstance(obs_dim, int):
            obs_dim = {"obs": obs_dim}

        self.state_modules_dict = make_models_for_obs(obs_dim=obs_dim,
                                                      hidden_dim=hidden_dim,
                                                      cnn_layers=cnn_layers,
                                                      activation=self.activation)

        self.critic_backbone = RecurrentBackbone(obs_dim=hidden_dim * len(obs_dim),
                                                 hidden_dim=hidden_dim,
                                                 dense_layers=dense_layers,
                                                 num_rnn_layers=num_rnn_layers,
                                                 rnn_type=rnn_type,
                                                 activation=activation,
                                                 layernorm=layernorm,
                                                 batch_first=False)
        f_ = self.critic_backbone.feature_dim
        value_dim = 1
        self.critic_head = PopArtValueHead(f_, value_dim)
        self.to(device)

    def forward(self, share_obs, rnn_states, masks):

        share_obs = check(share_obs).to(**self.tpdv)
        rnn_states = check(rnn_states).to(**self.tpdv)
        masks = check(masks).to(**self.tpdv)

        obs_ = dict(obs=share_obs)

        on_reset = masks
        state = torch.cat([m(obs_[k]) for k, m in self.state_modules_dict.items()], dim=-1)
        critic_features, critic_hx = self.critic_backbone(state, rnn_states, on_reset)

        critic = self.critic_head(critic_features)
        values = critic.squeeze(0)
        rnn_states = recursive_apply(critic_hx, lambda x: x.transpose(0, 1))

        return values, rnn_states
