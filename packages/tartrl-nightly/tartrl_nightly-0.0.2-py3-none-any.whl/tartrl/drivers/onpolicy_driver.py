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
from typing import Dict, Any, Optional
import numpy as np
import torch
from torch.nn.parallel import DistributedDataParallel

from tartrl.drivers.rl_driver import RLDriver

from tartrl.utils.util import _t2n
from tartrl.utils.logger import Logger
from tartrl.envs.wrappers.venv import VecInfo

class OnPolicyDriver(RLDriver):
    def __init__(
            self,
            config: Dict[str, Any],
            trainer,
            buffer,
            rank: int = 0,
            world_size: int = 1,
            client=None,
            logger: Optional[Logger] = None,
    ) -> None:

        self.trainer = trainer
        self.buffer = buffer
        self.learner_episode = -1
        self.actor_id = 0
        self.weight_ids = [0]
        self.world_size = world_size
        self.logger = logger

        args = config['args']
        self.program_type = args.program_type

        self.envs = config['envs']
        self.device = config['device']

        assert not (
                self.program_type != "actor" and self.world_size is None), "world size can not be none, get {}".format(
            world_size)

        self.num_agents = config['num_agents']

        # print(args)
        assert isinstance(
            rank, int), "rank must be int, but get {}".format(rank)
        self.rank = rank

        # for distributed learning
        assert not (world_size is None and self.program_type == 'learner'), "world_size must be int, but get {}".format(
            world_size)

        # parameters
        self.env_name = args.env_name
        self.algorithm_name = args.algorithm_name
        self.experiment_name = args.experiment_name
        self.concat_obs_as_share_obs = args.concat_obs_as_share_obs
        self.use_obs_instead_of_state = args.use_obs_instead_of_state
        self.num_env_steps = args.num_env_steps
        self.episode_length = args.episode_length
        self.n_rollout_threads = args.n_rollout_threads
        self.learner_n_rollout_threads = args.learner_n_rollout_threads

        self.n_eval_rollout_threads = args.n_eval_rollout_threads
        self.n_render_rollout_threads = args.n_render_rollout_threads
        self.use_linear_lr_decay = args.use_linear_lr_decay
        self.hidden_size = args.hidden_size
        self.use_wandb = not args.disable_wandb
        self.use_single_network = args.use_single_network
        self.use_render = args.use_render
        self.use_transmit = args.use_transmit
        self.recurrent_N = args.recurrent_N

        self.only_eval = args.only_eval
        # interval
        self.save_interval = args.save_interval
        self.use_eval = args.use_eval
        self.eval_interval = args.eval_interval
        self.log_interval = args.log_interval

        self.distributed_type = args.distributed_type

        self.actor_num = args.actor_num

        if self.distributed_type == 'async' and self.program_type == 'whole':
            print('can\'t use async mode when program_type is whole!')
            exit()

        if self.program_type in ["whole", "local"]:
            assert self.actor_num == 1, "when running actor and learner the same time, the actor number should be 1, but received {}".format(
                self.actor_num)
        # dir
        self.model_dir = args.model_dir
        if hasattr(args, "save_dir"):
            self.save_dir = args.save_dir

        self.args = args

    def _inner_loop(
            self,
    ) -> None:
        rollout_infos = self.actor_rollout()
        train_infos = self.learner_update()
        self.post_process()

        self.total_num_steps = (self.episode + 1) * \
                          self.episode_length * self.n_rollout_threads

        # rollout_infos can only be used when env is wrapped with VevMonitor
        self.logger.log_info(rollout_infos,step=self.total_num_steps)
        self.logger.log_info(train_infos,step=self.total_num_steps)


    def reset_and_buffer_init(self):
        # reset env
        returns = self.envs.reset()

        if isinstance(returns, tuple):
            assert len(returns) == 2, "length of env reset returns must be 2, but get {}".format(len(returns))
            obs, info = returns
        else:
            obs = returns

        share_obs = obs

        self.buffer.init_buffer(share_obs.copy(), obs.copy())

    def add2buffer(self, data):
        obs, rewards, dones, infos, values, actions, action_log_probs, rnn_states, rnn_states_critic = data

        rnn_states[dones == True] = np.zeros(((dones == True).sum(), self.recurrent_N, self.hidden_size),
                                             dtype=np.float32)

        rnn_states_critic[dones == True] = np.zeros(
            ((dones == True).sum(), *self.buffer.data.rnn_states_critic.shape[3:]), dtype=np.float32)
        masks = np.ones((self.n_rollout_threads, self.num_agents, 1), dtype=np.float32)
        masks[dones == True] = np.zeros(((dones == True).sum(), 1), dtype=np.float32)

        share_obs = obs

        self.buffer.insert(share_obs, obs, rnn_states, rnn_states_critic, actions, action_log_probs, values, rewards,
                           masks)

    def actor_rollout(self):

        self.trainer.prep_rollout()

        for step in range(self.episode_length):
            # Sample actions
            values, actions, action_log_probs, rnn_states, rnn_states_critic, actions_env = self.act(step)
            # Obser reward and next obs

            actions_env = np.argmax(actions_env[0][0])

            obs, rewards, dones, infos = self.envs.step(actions_env)

            data = obs, rewards, dones, infos, values, actions, action_log_probs, rnn_states, rnn_states_critic

            self.add2buffer(data)

        if self.envs.use_monitor:
            return self.envs.statistics()
        else:
            return {}


    def run(
            self
    ) -> None:
        episodes = int(self.num_env_steps) // self.episode_length // self.learner_n_rollout_threads
        self.episodes = episodes

        self.reset_and_buffer_init()

        for episode in range(episodes):
            self.logger.info("Episode: {}/{}".format(episode, episodes))
            self.episode = episode
            self._inner_loop()

    def learner_update(self):
        if self.use_linear_lr_decay:
            self.trainer.algo_module.lr_decay(self.episode, self.episodes)

        self.compute_returns()
        train_infos = self.train()
        return train_infos

    @torch.no_grad()
    def compute_returns(self):
        self.trainer.prep_rollout()

        next_values = self.trainer.algo_module.get_values(self.buffer.data.get_batch_data("share_obs", -1),
                                                          np.concatenate(
                                                              self.buffer.data.rnn_states_critic[-1]),
                                                          np.concatenate(self.buffer.data.masks[-1]))

        next_values = np.array(
            np.split(
                _t2n(next_values),
                self.learner_n_rollout_threads))
        if "critic" in self.trainer.algo_module.models and isinstance(
                self.trainer.algo_module.models["critic"], DistributedDataParallel):
            value_normalizer = self.trainer.algo_module.models["critic"].module.value_normalizer
        elif "model" in self.trainer.algo_module.models and isinstance(self.trainer.algo_module.models["model"],
                                                                       DistributedDataParallel):
            value_normalizer = self.trainer.algo_module.models["model"].module.value_normalizer
        else:
            value_normalizer = self.trainer.algo_module.get_critic_value_normalizer()
        self.buffer.compute_returns(next_values, value_normalizer)

    def train(self):
        self.trainer.prep_training()
        train_infos = self.trainer.train(self.buffer.data)
        return train_infos

    def post_process(self):
        self.buffer.after_update()

    @torch.no_grad()
    def act(
            self,
            step: int,
    ):
        self.trainer.prep_rollout()

        value, action, action_log_prob, rnn_states, rnn_states_critic \
            = self.trainer.algo_module.get_actions(self.buffer.data.get_batch_data("share_obs", step),
                                                   self.buffer.data.get_batch_data("obs", step),
                                                   np.concatenate(self.buffer.data.rnn_states[step]),
                                                   np.concatenate(self.buffer.data.rnn_states_critic[step]),
                                                   np.concatenate(self.buffer.data.masks[step]))

        # [self.envs, agents, dim]
        values = np.array(np.split(_t2n(value), self.n_rollout_threads))
        actions = np.array(np.split(_t2n(action), self.n_rollout_threads))
        action_log_probs = np.array(np.split(_t2n(action_log_prob), self.n_rollout_threads))
        rnn_states = np.array(np.split(_t2n(rnn_states), self.n_rollout_threads))
        rnn_states_critic = np.array(np.split(_t2n(rnn_states_critic), self.n_rollout_threads))
        # rearrange action
        if self.envs.action_space.__class__.__name__ == 'MultiDiscrete':
            for i in range(self.envs.action_space.shape):
                uc_actions_env = np.eye(self.envs.action_space.high[i] + 1)[actions[:, :, i]]
                if i == 0:
                    actions_env = uc_actions_env
                else:
                    actions_env = np.concatenate((actions_env, uc_actions_env), axis=2)
        elif self.envs.action_space.__class__.__name__ == 'Discrete':
            actions_env = np.squeeze(np.eye(self.envs.action_space.n)[actions], 2)
        else:
            actions_env = actions

        return values, actions, action_log_probs, rnn_states, rnn_states_critic, actions_env
