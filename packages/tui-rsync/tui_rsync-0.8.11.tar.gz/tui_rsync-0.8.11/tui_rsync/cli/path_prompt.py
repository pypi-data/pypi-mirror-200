################################################################################
# Copyright (C) 2023 Kostiantyn Klochko <kostya_klochko@ukr.net>               #
#                                                                              #
# This file is part of tui-rsync.                                              #
#                                                                              #
# tui-rsync is free software: you can redistribute it and/or modify it         #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# tui-rsync is distributed in the hope that it will be useful, but             #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY   #
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for  #
# more details.                                                                #
#                                                                              #
# You should have received a copy of the GNU General Public License along with #
# tui-rsync. If not, see <https://www.gnu.org/licenses/>.                      #
################################################################################

from sys import stderr
from rich.console import Console
from rich.prompt import Prompt
from pyfzf import FzfPrompt
import os
from tui_rsync.models.models import Destination, Path

console = Console()
err_console = Console(stderr=True)

class PathPrompt:
    @staticmethod
    def get_backup_fzf(label:str) -> str:
        dests_count = len(Destination.get_all(label))
        if dests_count == 0:
            err_console.print("[red b]No backups!!![/]")
            return ""
        if dests_count == 1:
            return Destination.get_all(label).get()
        fzf = FzfPrompt()
        return fzf.prompt(Destination.get_all(label).iterator())[0]
