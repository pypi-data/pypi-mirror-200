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
from tui_rsync.models.models import all_labels

console = Console()
source_remove = typer.Typer()

@source_remove.command()
def one(
    label: str = typer.Option(
        None, "--label", "-l",
        help="[b]The label[/] is a uniq identification of a [b]source[/].",
        show_default=False
    )
):
    """
    [red b]Remove[/] an [yellow]existing source[/].
    """
    if label is None:
        label = LabelPrompt.get_label_fzf()

    if Source.is_exist(label):
        src = Source.get_source(label)
        src.delete_instance()

@source_remove.command()
def all():
    """
    [red b]Remove[/] [yellow] all existing sources[/].
    """
    for label in all_labels().iterator():
        one(label.label)
