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
import typer
from tui_rsync.cli.source.source import source
from tui_rsync.cli.sync import sync
from tui_rsync.cli.groups.groups import groups

console = Console()
cli_app = typer.Typer(rich_markup_mode="rich")
cli_app.add_typer(source, name="source", help="Manage sources")
cli_app.add_typer(groups, name="groups", help="Manage groups")
cli_app.add_typer(sync, name="sync", help="Sync sources")

