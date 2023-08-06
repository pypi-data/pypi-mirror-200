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

import socket
from typing import Optional, Dict, Any
import os
import logging
from rich.logging import RichHandler
import wandb
from pathlib import Path
import numpy as np
import torch

class Logger:
    def __init__(
            self,
            args,
            project_name: str,
            scenario_name: str,
            wandb_entity: str,
            exp_name: str,
            log_path: Optional[str] = None,
            use_wandb: bool = False,
            use_tensorboard: bool = False,
            log_level: int = logging.DEBUG,
    ) -> None:
        self.use_wandb = use_wandb
        self.use_tensorboard = use_tensorboard

        self.log_level = log_level
        self.log_path = log_path
        self.project_name = project_name
        self.scenario_name = scenario_name
        self.wandb_entity = wandb_entity
        self.exp_name = exp_name
        self.args = args
        self._init()

    def _init(self) -> None:
        running_programs = ["learner", "server_learner", "local", "whole", "local_evaluator"]
        if not self.args.program_type in running_programs:
            return None

        if self.log_path is None:
            run_dir = Path(os.path.split(os.path.dirname(os.path.abspath(__file__)))[
                               0] + "/results") / self.project_name / self.scenario_name / self.args.algorithm_name / self.exp_name
        else:
            run_dir = Path(
                self.log_path) / self.project_name / self.scenario_name / self.args.algorithm_name / self.exp_name

        if not run_dir.exists():
            os.makedirs(str(run_dir))

        if not self.use_wandb:
            if not run_dir.exists():
                curr_run = 'run1'
            else:
                exst_run_nums = [int(str(folder.name).split('run')[1]) for folder in run_dir.iterdir() if
                                 str(folder.name).startswith('run')]
                if len(exst_run_nums) == 0:
                    curr_run = 'run1'
                else:
                    curr_run = 'run%i' % (max(exst_run_nums) + 1)
            run_dir = run_dir / curr_run
            if not run_dir.exists():
                os.makedirs(str(run_dir))

        if hasattr(self.args, "render"):
            self.args.render_save_path = run_dir / "render.png"

        log_path = os.path.join(run_dir, "log.txt")
        logging.basicConfig(
            level=self.log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_path),
                RichHandler()
            ]
        )

        if self.use_wandb:
            wandb.init(config=self.args,
                       project=self.project_name,
                       entity=self.wandb_entity,
                       notes=socket.gethostname(),
                       name=str(self.args.algorithm_name) + "_" +
                            str(self.exp_name) +
                            "_seed" + str(self.args.seed),
                       dir=str(run_dir),
                       job_type="training",
                       reinit=True)
        elif self.use_tensorboard:
            from tensorboardX import SummaryWriter
            self.log_dir = str(run_dir / 'logs')
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            self.writter = SummaryWriter(self.log_dir)

        self.run_dir = run_dir

    def close(self):
        if self.use_wandb:
            wandb.finish()

    def info(self, msg: str):
        logging.info(msg)

    def log_learner_info(
            self,
            leaner_id: int,
            infos: Dict[str, Any],
            step: int,
    ) -> None:
        for k, v in infos.items():
            if self.use_wandb:
                wandb.log({"Learner_{}/{}".format(leaner_id, k): v},
                          step=step)
            elif self.use_tensorboard:
                self.writter.add_scalars("Learner_{}/{}".format(leaner_id, k),
                                         {"Learner_{}/{}".format(leaner_id, k): v}, step)


    def log_info(
            self,
            infos: Dict[str, Any],
            step: int,
    ) -> None:
        for k, v in infos.items():
            # print(k,v)

            if isinstance(v,torch.Tensor):
                v = v.item()

            if not isinstance(v, (int,float)):
                v = np.mean(v)

            if self.use_wandb:
                wandb.log({k: v}, step=step)
            elif self.use_tensorboard:
                self.writter.add_scalars(
                    k, {k: v}, step)


if __name__ == "__main__":
    from collections import namedtuple

    ARG = namedtuple("args", ["seed", "algorithm_name", "program_type"])

    class Namespace(ARG):
        @property
        def __dict__(self):
            return self._asdict()


    args = Namespace(seed=1, algorithm_name="algorithm", program_type="local")

    logger = Logger(
        args=args,
        project_name="test_logger",
        scenario_name="logger",
        wandb_entity="tmarl",
        exp_name="test",
        log_path="../../../test_logger/",
        use_wandb=False,
        use_tensorboard=True,
    )
    for step in range(100):
        logger.log_info({"test": step}, step)
        logger.log_info({"test2": [step,2*step]}, step)
        logger.log_info({"test3": np.random.random((10,10))}, step)
    logger.info("hello")
    logger.close()
