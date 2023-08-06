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

from tui_rsync.models.models import Source, Group, Destination, SyncCommand
from tui_rsync.models.models import Path
from tui_rsync.models.models import all_labels
from tui_rsync.cli.label_prompt import LabelPrompt
from tui_rsync.cli.groups.group_prompt import GroupPrompt
from tui_rsync.cli.path_prompt import PathPrompt
from tui_rsync.cli.rsync import Rsync

console = Console()
sync = typer.Typer()

skip_error = "[yellow b]Skippped[/] because the [red b]path was unavailable[/]."

@sync.command()
def one(
    label: str = typer.Option(
        None, "--label", "-l",
        help="[b]The label[/] is a uniq identification of a [b]source[/].",
        show_default=False
    ),
    dry: bool = typer.Option(
        False, "-d", "--dry-run",
        help="The command will [b]show[/] information about what will be changed.",
    )
):
    """
    [green b]Sync[/] a [yellow]source[/] with the [yellow b]label[/] and its backups.
    [yellow b]Skips[/] if not available.
    """
    if label is None:
        label = LabelPrompt.get_label_fzf()
    src = Source.get_source(label)
    rsync = Rsync(str(src.args))
    for dest in src.destinations:
        if not dest.path.is_exists():
            console.print(skip_error)
            continue
        if dry:
            response = rsync.dry_one(str(src.source), str(dest))
            out, err = response
            console.print(f"{bstr_nonan(out)} {bstr_nonan(err)}")
        else:
            rsync.run_one(str(src.source), str(dest))

@sync.command()
def group(
    group_label: str = typer.Option(
        None, "--group-label", "-g",
        help="[b]The label[/] is a uniq identification of a [b]group[/].",
        show_default=False
    ),
):
    """
    [green b]Sync[/] a [yellow]group[/] with the [yellow b] label[/].
    """
    if group_label is None:
        group_label = GroupPrompt.get_label_fzf()
    group = Group.get_group(group_label)

    for src in group.get_sources():
        one(src.label)

@sync.command()
def all():
    """
    [green b]Sync[/] [yellow]all sources[/] with theirs backups.
    """
    for label in all_labels().iterator():
        one(label.label)

@sync.command()
def recover(
    label: str = typer.Option(
        None, "--label", "-l",
        help="[b]The label[/] is a uniq identification of a [b]source[/].",
        show_default=False
    ),
):
    """
    [green b]Sync[/] the [yellow]chosen backup[/] with its source.
    """
    if label is None:
        label = LabelPrompt.get_label_fzf()
    src = Source.get(Source.label == label)
    dest = PathPrompt.get_backup_fzf(label)

    rsync = Rsync(str(src.args))
    rsync.run_one(str(dest), str(src.source))

def bstr_nonan(obj):
    return "" if obj is None else obj.decode()
