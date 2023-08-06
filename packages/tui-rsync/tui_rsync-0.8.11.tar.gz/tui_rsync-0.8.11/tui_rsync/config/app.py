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

import platformdirs
import os

class App:
    """
    Configuration of the tui-rsync
    """
    __APP_NAME = "tui-rsync"
    __APP_AUTHOR = "KKlochko"
    __DB_NAME = "sync.db"

    def get_db_path(self):
        path = platformdirs.user_data_path(
            self.__APP_NAME,
            self.__APP_AUTHOR,
            self.__DB_NAME
        )
        App.safe_create_path(self.get_data_dir())
        return path

    def get_data_dir(self):
        return platformdirs.user_data_dir(
            self.__APP_NAME,
            self.__APP_AUTHOR,
        )

    @staticmethod
    def safe_create_path(path):
        """
        Create path's folders if they do not exist
        """
        if not os.path.exists(path):
            os.makedirs(path)
