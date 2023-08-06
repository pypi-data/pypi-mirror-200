from abc import ABC, abstractmethod
import torch


class BaseAlgorithm(ABC):
    def __init__(self,
                 args,
                 init_module,
                 device=torch.device("cpu")):
        self.all_args = args

        if isinstance(device, str):
            device = torch.device(device)

        self.device = device
        self.tpdv = dict(dtype=torch.float32, device=device)

        self.algo_module = init_module

        self.world_size = self.algo_module.world_size
        self.clip_param = args.clip_param
        self.ppo_epoch = args.ppo_epoch
        self.num_mini_batch = args.num_mini_batch
        self.data_chunk_length = args.data_chunk_length
        self.policy_value_loss_coef = args.policy_value_loss_coef
        self.value_loss_coef = args.value_loss_coef
        self.entropy_coef = args.entropy_coef
        self.max_grad_norm = args.max_grad_norm
        self.huber_delta = args.huber_delta

        self._use_recurrent_policy = args.use_recurrent_policy
        self._use_naive_recurrent = args.use_naive_recurrent_policy
        self._use_max_grad_norm = args.use_max_grad_norm
        self._use_clipped_value_loss = args.use_clipped_value_loss
        self._use_huber_loss = args.use_huber_loss
        self._use_popart = args.use_popart
        self._use_valuenorm = args.use_valuenorm
        self._use_value_active_masks = args.use_value_active_masks
        self._use_policy_active_masks = args.use_policy_active_masks
        self._use_policy_vhead = args.use_policy_vhead
        self._use_new_network = hasattr(
            args, "use_new_network") and args.use_new_network
        self._num_agents = args.num_agents

        self._use_adv_normalize = args.use_adv_normalize

        # for tranformer
        self.dec_actor = args.dec_actor

        self.use_amp = args.use_amp

        self.dual_clip_ppo = args.dual_clip_ppo
        self.dual_clip_coeff = torch.tensor(
            args.dual_clip_coeff).to(
            self.device)

        assert not (self._use_popart and self._use_valuenorm), (
            "self._use_popart and self._use_valuenorm can not be set True simultaneously")

    @abstractmethod
    def train(self, buffer, turn_on=True):
        raise NotImplementedError

    def prep_training(self):
        for model in self.algo_module.models.values():
            model.train()

    def prep_rollout(self):
        for model in self.algo_module.models.values():
            model.eval()
