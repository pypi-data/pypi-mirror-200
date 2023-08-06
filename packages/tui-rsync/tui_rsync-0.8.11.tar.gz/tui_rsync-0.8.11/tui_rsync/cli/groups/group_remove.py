################################################################################
# Copyright (C) 2023 Kostiantyn Klochko <kostya_klochko@ukr.net>               #
#                                                                              #
# This file is part of tui-rsync.                                              #
#                                                                              #
# tui-rsync is free software: you can redistribute it and/or modify it under   #
# uthe terms of the GNU General Public License as published by the Free        #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# tui-rsync is distributed in the hope that it will be useful, but WITHOUT ANY #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more        #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU General Public License along with #
# tui-rsync. If not, see <https://www.gnu.org/licenses/>.                      #
################################################################################

from rich.console import Console
from rich.prompt import Prompt
from typing import List, Optional
import typer

from tui_rsync.models.models import Group
from tui_rsync.models.models import all_group_labels
from tui_rsync.cli.groups.group_prompt import GroupPrompt

console = Console()
group_remove = typer.Typer()

@group_remove.command()
def one(
    group_label: str = typer.Option(
        None, "--group-label", "-g",
        help="[b]The label[/] is a uniq identification of a [b]group[/].",
        show_default=False
    ),
):
    """
    [red b]Remove[/] an [yellow]existing group[/].
    """
    if group_label is None:
        group_label = GroupPrompt.get_label_fzf()

    if Group.is_exist(group_label):
        group = Group.get_group(group_label)
        group.delete_instance()

@group_remove.command()
def all():
    """
    [red b]Remove[/] [yellow] all existing groups[/].
    """
    for label in all_group_labels().iterator():
        one(label.label)
