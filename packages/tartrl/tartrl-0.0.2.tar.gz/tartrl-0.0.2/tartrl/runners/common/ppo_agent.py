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
import pathlib

from typing import Union, Dict, Tuple, Optional

import numpy as np
import torch
import gym

from tartrl.runners.common.base_agent import BaseAgent
from tartrl.runners.common.base_agent import SelfAgent

from tartrl.drivers.onpolicy_driver import OnPolicyDriver as Driver
from tartrl.algorithms.ppo import PPOAlgorithm as TrainAlgo
from tartrl.buffers import NormalReplayBuffer as ReplayBuffer
from tartrl.utils.logger import Logger

class PPOAgent(BaseAgent):
    def __init__(
            self,
            net: Optional[torch.nn.Module] = None,
            env: Union[gym.Env, str] = None,
            run_dir: str = "./",
            n_rollout_threads: Optional[int] = None,
            rank: int = 0,
            world_size: int = 1,
            agent_num: int = 1,
            use_wandb: bool = False,
            use_tensorboard: bool = False,
    ) -> None:
        self.net = net
        self._args = net.args
        self._use_wandb = use_wandb
        self._use_tensorboard = not use_wandb and use_tensorboard

        if n_rollout_threads is not None:
            self._args.n_rollout_threads = n_rollout_threads

        if env is not None:
            self._env = env
        elif hasattr(net, "env") and net.env is not None:
            self._env = net.env
        else:
            raise ValueError("env is None")

        self.rank = rank
        self.world_size = world_size

        self.client = None
        self.agent_num = agent_num
        self.run_dir = run_dir

    def train(
            self: SelfAgent,
            total_time_steps: int
    ) -> None:

        self._args.num_env_steps = total_time_steps

        self.config = {
            "args": self._args,
            "num_agents": self.agent_num,
            "run_dir": self.run_dir,
            'envs': self._env,
            'device': self.net.device,
        }

        trainer = TrainAlgo(
            args=self._args,
            init_module=self.net.module,
            device=self.net.device)

        share_observation_space = self._env.observation_space

        buffer = ReplayBuffer(
            self._args,
            self.agent_num,
            self._env.observation_space,
            share_observation_space,
            self._env.action_space,
            data_client=None,
        )

        logger = Logger(
            args = self._args,
            project_name="PPOAgent",
            scenario_name=self._env.env_name,
            wandb_entity=self._args.wandb_entity,
            exp_name="ppo",
            log_path="../../../ppo_agent_logger/",
            use_wandb=self._use_wandb,
            use_tensorboard=self._use_tensorboard,
        )
        driver = Driver(
            config=self.config,
            trainer=trainer,
            buffer=buffer,
            client=self.client,
            rank=self.rank,
            world_size=self.world_size,
            logger = logger,
        )
        driver.run()

    def act(
            self,
            observation: Union[np.ndarray, Dict[str, np.ndarray]],
            deterministic: bool = False,
    ) -> Tuple[np.ndarray, Optional[Tuple[np.ndarray, ...]]]:
        assert self.net is not None, "net is None"
        return self.net.act(observation, deterministic=deterministic)


    def reset(self) -> None:
        self.net.reset()

    def save(self, path: Union[str, pathlib.Path, io.BufferedIOBase]) -> None:
        pass
