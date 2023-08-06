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

from typing import Union, Tuple, Dict, Optional

import numpy as np
import gym
import torch

from tartrl.modules.ppo_module import PPOModule
from tartrl.configs.config import build_parser
from tartrl.modules.common.base_net import BaseNet

class PPONet(BaseNet):
    def __init__(
            self,
            env: Union[gym.Env, str],
            device: Union[torch.device, str] = 'cpu',
            n_rollout_threads: int = 1,
    ) -> None:
        super().__init__()
        parser = build_parser()
        args = parser.parse_known_args("")[0]
        args.n_rollout_threads = n_rollout_threads
        args.learner_n_rollout_threads = args.n_rollout_threads

        if args.rnn_type == "gru":
            rnn_hidden_size = args.hidden_size
        elif args.rnn_type == "lstm":
            rnn_hidden_size =args.hidden_size * 2
        else:
            raise NotImplementedError(
                f'RNN type {args.rnn_type} has not been implemented.')
        args.rnn_hidden_size = rnn_hidden_size

        if isinstance(device, str):
            device = torch.device(device)

        self.module = PPOModule(
            args=args,
            policy_input_space=env.observation_space,
            critic_input_space=env.observation_space,
            act_space=env.action_space,
            share_model=False,
            device=device,
            rank=0,
            world_size=1,
        )

        self.args = args
        self.env = env
        self.device = device
        self.rnn_states_actor = None
        self.masks = None

    def act(
            self,
            observation: Union[np.ndarray, Dict[str, np.ndarray]],
            deterministic: bool = False,
    ) -> Tuple[np.ndarray, Optional[Tuple[np.ndarray, ...]]]:

        if not self.first_reset:
            self.reset()

        actions, self.rnn_states_actor = self.module.act(
            obs = observation,
            rnn_states_actor=self.rnn_states_actor,
            masks=self.masks,
            available_actions=None,
            deterministic=deterministic,
        )

        actions = actions.item()

        return actions, self.rnn_states_actor

    def reset(self):
        self.first_reset = False
        self.rnn_states_actor, self.masks = self.module.init_rnn_states(
            rollout_num=self.args.n_rollout_threads,
            agent_num=self.env.agent_num,
            rnn_layers=self.args.recurrent_N,
            hidden_size=self.args.rnn_hidden_size,
        )

