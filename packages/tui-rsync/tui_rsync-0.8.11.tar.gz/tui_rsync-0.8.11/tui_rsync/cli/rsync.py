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

import shlex
from subprocess import Popen, PIPE

class Rsync:
    def __init__(self, args:str):
        self.__args = ["rsync"] + shlex.split(args)

    def run_one(self, source, destination):
        args = self.__args + [source, destination]
        output = Popen(args, stdout=PIPE)
        response = output.communicate()

    def dry_one(self, source, destination):
        args = self.__args + ['--dry-run', source, destination]
        output = Popen(args, stdout=PIPE)
        response = output.communicate()
        return response
