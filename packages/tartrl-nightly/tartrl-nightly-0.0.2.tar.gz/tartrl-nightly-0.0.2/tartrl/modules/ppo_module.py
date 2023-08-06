#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2023 The TARTRL Authors.
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

from typing import Optional, Union

import numpy as np
import gym
import torch

from tartrl.modules.rl_module import RLModule
from tartrl.modules.model_config import ModelTrainConfig

from tartrl.modules.networks.policy_value_network import PolicyValueNetwork
from tartrl.modules.networks.policy_network import PolicyNetwork
from tartrl.modules.networks.value_network import ValueNetwork
from tartrl.modules.utils.util import update_linear_schedule


class PPOModule(RLModule):
    def __init__(
            self,
            args,
            policy_input_space: gym.spaces.Box,
            critic_input_space: gym.spaces.Box,
            act_space: gym.spaces.Box,
            share_model: bool = False,
            device: Union[str, torch.device] = "cpu",
            rank: Optional[int] = None,
            world_size: Optional[int] = None,
    ):
        model_configs = {}
        if share_model:
            model_configs["model"] = ModelTrainConfig(
                lr=args.lr,
                model=PolicyValueNetwork,
                input_space=policy_input_space,
            )
        else:
            model_configs["policy"] = ModelTrainConfig(
                lr=args.lr,
                model=PolicyNetwork,
                input_space=policy_input_space,
            )
            model_configs["critic"] = ModelTrainConfig(
                lr=args.critic_lr,
                model=ValueNetwork,
                input_space=critic_input_space,
            )

        super(PPOModule, self).__init__(
            args=args,
            model_configs=model_configs,
            act_space=act_space,
            rank=rank,
            world_size=world_size,
            device=device,
        )
        self.share_model = share_model
        self.args = args

    def lr_decay(self, episode, episodes):
        if self.share_model:
            update_linear_schedule(self.optimizers['model'], episode, episodes, self.lr)
        else:
            update_linear_schedule(self.optimizers['actor'], episode, episodes, self.lr)
            update_linear_schedule(self.optimizers['critic'], episode, episodes, self.critic_lr)

    def get_actions(self, share_obs, obs, rnn_states_actor, rnn_states_critic, masks, available_actions=None,
                    deterministic=False):
        if self.share_model:
            raise NotImplementedError
        else:
            actions, action_log_probs, rnn_states_actor = self.models['policy']("original", obs, rnn_states_actor, masks,
                                                                                available_actions, deterministic)

            values, rnn_states_critic = self.models['critic'](share_obs, rnn_states_critic, masks)
        return values, actions, action_log_probs, rnn_states_actor, rnn_states_critic

    def get_values(self, share_obs, rnn_states_critic, masks):
        if self.share_model:
            raise NotImplementedError
        else:
            values, _ = self.models['critic'](share_obs, rnn_states_critic, masks)
        return values

    def evaluate_actions(self, share_obs, obs, rnn_states_actor, rnn_states_critic, action, masks,
                         available_actions=None, active_masks=None, critic_masks_batch=None):
        if critic_masks_batch is None:
            critic_masks_batch = masks

        if self.share_model:
            raise NotImplementedError
        else:
            values, _ = self.models['critic'](share_obs, rnn_states_critic, critic_masks_batch)

            action_log_probs, dist_entropy, policy_values = self.models['policy'](
                "eval_actions",
                obs,
                rnn_states_actor,
                action,
                masks,
                available_actions,
                active_masks,
            )

        return values, action_log_probs, dist_entropy, policy_values

    def act(self, obs, rnn_states_actor, masks, available_actions=None, deterministic=False):
        if self.share_model:
            raise NotImplementedError
        else:
            actions, _, rnn_states_actor = self.models['policy'](
                "original",
                obs,
                rnn_states_actor,
                masks,
                available_actions,
                deterministic,
            )
        return actions, rnn_states_actor

    def get_critic_value_normalizer(self):
        if self.share_model:
            raise NotImplementedError
        else:
            return self.models["critic"].value_normalizer

    @staticmethod
    def init_rnn_states(rollout_num: int,
                             agent_num: int,
                             rnn_layers: int,
                             hidden_size: int
                             ):
        masks = np.ones((rollout_num*agent_num, 1), dtype=np.float32)
        rnn_state = np.zeros((rollout_num*agent_num, rnn_layers, hidden_size))
        return rnn_state, masks
