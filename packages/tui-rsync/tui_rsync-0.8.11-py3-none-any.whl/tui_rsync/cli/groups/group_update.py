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

from tui_rsync.models.models import Group, GroupSource
from tui_rsync.cli.label_prompt import LabelPrompt
from tui_rsync.cli.groups.group_prompt import GroupPrompt
from typer.main import get_group

console = Console()
group_update = typer.Typer()

@group_update.command()
def label(
    group_label: str = typer.Option(
        None, "--group-label", "-l",
        help="[b]The label[/] is a uniq identification of a [b]group[/].",
        show_default=False
    ),
    new_group_label: str = typer.Option(
        None, "--new-group-label", "-nl",
        help="[b]The new label[/] will replace the [b]old group label[/].",
        show_default=False
    ),

):
    """
    [green b]Update[/] an [yellow]existing group label[/].
    """
    if group_label is None:
        console.print("What is the [yellow b]old label of group[/]? ")
        group_label = GroupPrompt.get_label_fzf()

    if new_group_label is None:
        question = "What is the [yellow b]new label of the group[/]? "
        new_group_label = GroupPrompt.ask_uuid(question)

    if Group.is_exist(group_label):
        group = Group.get_group(group_label)
        group.update_label(new_group_label)

@group_update.command()
def labels(
    group_label: str = typer.Option(
        None, "--group-label", "-g",
        help="[b]The label[/] is a uniq identification of a [b]group[/].",
        show_default=False
    ),
    new_labels: str = typer.Option(
        None, "--new-labels", "-nl",
        help="[b]The new label[/] will replace the [b]old source label[/].",
        show_default=False
    ),

):
    """
    [green b]Update[/] [yellow]the group[/] with a [bold]the label[/].
    [b]The chosen sources[/] will be updated for [b]the group[/].
    """
    if group_label is None:
        group_label = GroupPrompt.get_label_fzf()

    if new_labels is None:
        new_labels = LabelPrompt.get_labels()

    group = Group.get_group(group_label)
    group.remove_sources()
    GroupSource.create_group_sources(group, new_labels)
    group.save()
