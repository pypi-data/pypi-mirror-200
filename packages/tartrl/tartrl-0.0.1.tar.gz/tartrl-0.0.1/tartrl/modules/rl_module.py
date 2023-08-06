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
from abc import abstractmethod
from typing import Dict, Union

import torch
from gym import spaces
from pathlib import Path

from tartrl.modules.base_module import BaseModule
from tartrl.modules.model_config import ModelTrainConfig


class RLModule(BaseModule):
    def __init__(self,
                 args,
                 model_configs: Dict[str, ModelTrainConfig],
                 act_space: spaces.Box,
                 rank: int = 0,
                 world_size: int = 1,
                 device: Union[str, torch.device] = "cpu",
                 ) -> None:

        super(RLModule, self).__init__(args)

        if isinstance(device, str):
            device = torch.device(device)

        self.device = device
        self.lr = args.lr
        self.critic_lr = args.critic_lr
        self.opti_eps = args.opti_eps
        self.weight_decay = args.weight_decay
        self.load_optimizer = args.load_optimizer

        self.act_space = act_space

        self.program_type = args.program_type
        self.rank = rank
        self.world_size = world_size
        self.use_new_network = hasattr(args, "use_new_network") and args.use_new_network

        use_half_actor = self.program_type == "actor" and args.use_half_actor

        for model_key in model_configs:
            model_cg = model_configs[model_key]
            model = model_cg["model"](
                args=args,
                input_space=model_cg["input_space"],
                action_space=act_space,
                device=device,
                use_half=use_half_actor,
            )
            self.models.update({model_key: model})

            if self.program_type == "actor":
                continue

            optimizer = torch.optim.Adam(
                model.parameters(),
                lr=model_cg["lr"],
                eps=args.opti_eps,
                weight_decay=args.weight_decay,
            )
            self.optimizers.update({model_key: optimizer})

            if args.use_amp:
                self.scaler = torch.cuda.amp.GradScaler()
            else:
                self.scaler = None

    @abstractmethod
    def get_actions(self, share_obs, obs, rnn_states_actor, rnn_states_critic, masks, available_actions=None,
                    deterministic=False):

        raise NotImplementedError

    @abstractmethod
    def get_values(self, share_obs, rnn_states_critic, masks):
        raise NotImplementedError

    @abstractmethod
    def evaluate_actions(self, share_obs, obs, rnn_states_actor, rnn_states_critic, action, masks,
                         available_actions=None, active_masks=None, critic_masks_batch=None):
        raise NotImplementedError

    @abstractmethod
    def act(self, obs, rnn_states_actor, masks, available_actions=None, deterministic=False):
        raise NotImplementedError

    @abstractmethod
    def get_critic_value_normalizer(self):
        raise NotImplementedError

    def restore(self, model_dir: str) -> None:
        model_dir = Path(model_dir)
        assert model_dir.exists(), "can not find model directory to restore: {}".format(model_dir)

        for model_name in self.models:
            state_dict = torch.load(str(model_dir) + '/{}.pt'.format(model_name), map_location=self.device)
            self.models[model_name].load_state_dict(state_dict)
            del state_dict

        if self.load_optimizer:
            if Path(str(model_dir) + '/actor_optimizer.pt').exists():
                for optimizer_name in self.optimizers:
                    state_dict = torch.load(str(model_dir) + '/{}_optimizer.pt'.format(optimizer_name),
                                            map_location=self.device)
                    self.optimizers[optimizer_name].load_state_dict(state_dict)
                    del state_dict
            else:
                print("can't find optimizer to restore")
        # TODO
        # optimizer.load_state_dict(resume_state['optimizer'])

    def save(self, save_dir: str) -> None:
        pass
