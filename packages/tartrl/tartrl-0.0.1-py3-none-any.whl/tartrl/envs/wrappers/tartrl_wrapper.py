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
from typing import Any
import gymnasium as gym
import numpy as np


class TARTRLWrapper(gym.Wrapper):
    @property
    def env_name(self):
        if hasattr(self.env, "env_name"):
            return self.env.env_name
        return self.env.unwrapped.spec.id

    @property
    def agent_num(self):
        if hasattr(self.env, "agent_num"):
            return self.env.agent_num
        else:
            raise NotImplementedError("Not support agent_num")

    @property
    def use_monitor(self):
        return False


class TARTRLObservationWrapper(TARTRLWrapper, gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)


class DictWrapper(TARTRLObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        need_convert = 'Dict' not in self.env.observation_space.__class__.__name__
        if need_convert:
            self.observation_space = gym.spaces.Dict(
                {
                    "obs": self.env.observation_space,
                }
            )

    def observation(self, observation):
        return {
            "obs": observation,
            "share_obs": observation
        }


class MultiAgentWrapper(TARTRLWrapper):
    def __init__(self, env):
        super().__init__(env)
        self._agent_num = 1

    @property
    def agent_num(self):
        return self._agent_num

    def reset(self, *, seed, options=None):

        returns = self.env.reset(seed=seed, options=options)

        if isinstance(returns, tuple):
            if len(returns) == 2:
                # obs, info
                return nest_expand_dim(returns[0]), returns[1]
            else:
                raise NotImplementedError("Not support reset return length: {}".format(len(returns)))
        else:
            return nest_expand_dim(returns)

    def step(self, action):
        returns = self.env.step(action)

        assert isinstance(returns, tuple), "step return must be tuple, but got: {}".format(type(returns))

        if len(returns) == 4:
            # obs reward done info
            return nest_expand_dim(returns[0]), nest_expand_dim(returns[1]), nest_expand_dim(returns[2]), returns[3]
        elif len(returns) == 5:
            # obs reward done truncated, info
            return nest_expand_dim(returns[0]), nest_expand_dim(returns[1]), nest_expand_dim(
                returns[2]), nest_expand_dim(returns[3]), \
                returns[4]
        else:
            raise NotImplementedError("Not support step return length: {}".format(len(returns)))


def nest_expand_dim(input: Any) -> Any:
    if isinstance(input, (np.ndarray, float, int)):
        return np.expand_dims(input, 0)
    elif isinstance(input, list):
        return [input]
    elif isinstance(input, dict):
        for key in input:
            input[key] = nest_expand_dim(input[key])
        return input
    else:
        raise NotImplementedError("Not support type: {}".format(type(input)))
