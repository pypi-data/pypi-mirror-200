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

import click
from click.core import Context, Option

from tartrl import __TITLE__, __VERSION__, __AUTHOR__, __EMAIL__
from termcolor import colored

def red(text: str):
    return colored(text, 'red')

def print_version(
        ctx: Context,
        param: Option,
        value: bool,
) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.secho(f"{__TITLE__.upper()} version: {red(__VERSION__)}")
    click.secho(f"Developed by {__AUTHOR__}, Email: {red(__EMAIL__)}")
    ctx.exit()


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--version',
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show package's version information."
)
@click.option(
    '--mode',
    prompt='Choose execution mode',
    type=click.Choice(
        [
            'train',
        ]
    ),
    help='execution mode'
)
@click.option('--env', prompt='Please enter environment name', type=str, help='RL environment name')
def run(
        mode: str,
        env: str
):
    if mode == "train":
        from tartrl.cli.train import train_agent
        train_agent(env)
    else:
        raise NotImplementedError
