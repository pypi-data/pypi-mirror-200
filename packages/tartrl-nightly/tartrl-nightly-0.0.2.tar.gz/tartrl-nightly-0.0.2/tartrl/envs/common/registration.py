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
import gymnasium as gym
from gymnasium import Env
from gymnasium.wrappers import (
    StepAPICompatibility,
    AutoResetWrapper,
)

from tartrl.envs.wrappers import (
    DictWrapper,
    MultiAgentWrapper,
    SingleEnv,
    VecMonitor,
)


def make(
        id: str,
        add_monitor: bool = True,
        *args,
        **kwargs,
) -> Env:
    env = gym.make(id, *args, **kwargs)
    env = MultiAgentWrapper(env)
    env = DictWrapper(env)
    env = AutoResetWrapper(env)
    env = StepAPICompatibility(
        env,
        output_truncation_bool=False
    )
    env = SingleEnv(env)
    if add_monitor:
        env = VecMonitor(env)

    return env
