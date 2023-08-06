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
from tui_rsync.cli.source.source_update import source_update
from tui_rsync.cli.source.source_remove import source_remove

console = Console()
source = typer.Typer()
source.add_typer(source_update, name="update", help="Update sources")
source.add_typer(source_remove, name="remove", help="Remove sources")

@source.command()
def add(
    label: str = typer.Option(
        None, "--label", "-l",
        help="[b]The label[/] is a uniq identification of a [b]source[/].",
        show_default=False
    ),
    source: str = typer.Option(
        None, "--source", "-s",
        help="[b]A source[/] of the data.",
        show_default=False
    ),
    destinations: Optional[List[str]] = typer.Option(
        None, "--destination", "-d", help="[b]The backup[/] destinations.",
        show_default=False
    ),
    args: str = typer.Option(
        None, "--args", "-a",
        help="[b i yellow]Additional[/] rsync [b]arguments[/].",
        show_default=False
    )
):
    """
    [green b]Create[/] a [yellow]new source[/] with a [bold]uniq[/] label.
    [b]The source[/] will be connected to [b]backup destinations[/].
    [yellow i]Optionally, additional[/] arguments for rsync can be added.
    """
    if label is None:
        label = LabelPrompt.ask_uuid()
    if source is None:
        source = console.input("What is the [yellow b]path to the source[/]? ")
    if args is None:
        args = console.input("What is the [yellow b]rsync args of source[/]? ")
    Source.create_save(label, source, destinations, args)

