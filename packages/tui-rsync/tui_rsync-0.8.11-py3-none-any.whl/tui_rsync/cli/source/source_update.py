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

from tui_rsync.models.models import Source, Destination, SyncCommand, Path
from tui_rsync.cli.label_prompt import LabelPrompt

console = Console()
source_update = typer.Typer()

@source_update.command()
def label(
    label: str = typer.Option(
        None, "--label", "-l",
        help="[b]The label[/] is a uniq identification of a [b]source[/].",
        show_default=False
    ),
    new_label: str = typer.Option(
        None, "--new-label", "-nl",
        help="[b]The new label[/] will replace the [b]old source label[/].",
        show_default=False
    ),

):
    """
    [green b]Update[/] an [yellow]existing source label[/].
    """
    if label is None:
        console.print("What is the [yellow b]old label of source[/]? ")
        label = LabelPrompt.get_label_fzf()

    if new_label is None:
        question = "What is the [yellow b]new label of the source[/]? "
        new_label = LabelPrompt.ask_uuid(question)

    if Source.is_exist(label):
        src = Source.get_source(label)
        src.update_label(new_label)

@source_update.command()
def args(
    label: str = typer.Option(
        None, "--label", "-l",
        help="[b]The label[/] is a uniq identification of a [b]source[/].",
        show_default=False
    ),
    args: str = typer.Option(
        None, "--args", "-a",
        help="[b yellow]rsync[/] [b]arguments[/].",
        show_default=False
    )

):
    """
    [green b]Update[/] an [yellow]existing source args[/].
    """
    if args is None:
        args = console.input("What is the [yellow b]rsync args of source[/]? ")

    if Source.is_exist(label):
        src = Source.get_source(label)
        src.update_args(args)

