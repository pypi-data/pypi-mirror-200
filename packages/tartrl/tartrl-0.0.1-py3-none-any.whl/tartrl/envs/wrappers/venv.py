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
from typing import Dict, Any
from gymnasium.core import ActType
import numpy as np

from .tartrl_wrapper import nest_expand_dim
from .tartrl_wrapper import TARTRLWrapper

class VecInfo:
    def __init__(self, parallel_env_num, agent_num):
        self.parallel_env_num = parallel_env_num
        self.agent_num = agent_num

        self.infos = []
        self.rewards = []

    def statistics(self) -> Dict[str, Any]:

        rewards = np.array(self.rewards).transpose(2,0,1)
        info_dict = {}
        for i in range(self.agent_num):
            info_dict["agent_{}/episode_reward".format(i)] = rewards[i].sum()
        return info_dict

    def append(self,reward,info):
        assert reward.shape[:2] == (self.parallel_env_num, self.agent_num)
        self.infos.append(info)
        self.rewards.append(reward)


    def reset(self):
        self.infos = []
        self.rewards = []


class BaseVecEnv(TARTRLWrapper):
    def __init__(
            self,
            env,
            parallel_env_num: int
    ) -> None:
        self.parallel_env_num = parallel_env_num
        super().__init__(env)

class VecMonitor(TARTRLWrapper):
    def __init__(self, env: BaseVecEnv):
        super().__init__(env)
        self.vec_info = VecInfo(
            self.env.parallel_env_num,
            self.env.agent_num
        )

    @property
    def use_monitor(self):
        return True

    def step(
            self,
            action: ActType
    ):
        returns = self.env.step(action)

        self.vec_info.append(
            reward = returns[1],
            info = returns[-1]
        )

        return returns

    def statistics(self):
        info_dict = self.vec_info.statistics()
        self.vec_info.reset()
        return info_dict


class SingleEnv(BaseVecEnv):
    def __init__(self, env):
        super().__init__(
            env=env,
            parallel_env_num=1
        )

    def reset(self, *, seed, options=None):

        returns = self.env.reset(seed=seed, options=options)

        if isinstance(returns, tuple):
            if len(returns) == 2:
                # obs, info
                return nest_expand_dim(returns[0]), [returns[1]]
            else:
                raise NotImplementedError("Not support reset return length: {}".format(len(returns)))
        else:
            return nest_expand_dim(returns)

    def step(
            self,
            action: ActType
    ):
        returns = self.env.step(action)

        assert isinstance(returns, tuple), "step return must be tuple, but got: {}".format(type(returns))

        if len(returns) == 4:
            # obs reward done info
            return nest_expand_dim(returns[0]), nest_expand_dim(returns[1]), nest_expand_dim(returns[2]), [returns[3]]
        elif len(returns) == 5:
            # obs reward done truncated, info
            return nest_expand_dim(returns[0]), nest_expand_dim(returns[1]), nest_expand_dim(
                returns[2]), nest_expand_dim(returns[3]), \
                [returns[4]]
        else:
            raise NotImplementedError("Not support step return length: {}".format(len(returns)))
