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
import io
from typing import Union, Type, TypeVar
from abc import ABC, abstractmethod
import pathlib

SelfAgent = TypeVar("SelfAgent", bound="BaseAgent")

SelfBaseAgent = TypeVar("SelfBaseAgent", bound="BaseAgent")

class BaseAgent(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self, path: Union[str, pathlib.Path, io.BufferedIOBase], ) -> None:
        raise NotImplementedError

    @classmethod
    def load(
            cls: Type[SelfBaseAgent],
            path: Union[str, pathlib.Path, io.BufferedIOBase],
    ) -> SelfBaseAgent:
        agent = cls()
        return agent
