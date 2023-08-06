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

from peewee import *
from tui_rsync.config.app import App
import os

app = App()
db = SqliteDatabase(app.get_db_path())

class BaseModel(Model):
    class Meta:
        database = db

class Path(BaseModel):
    path = CharField(unique=True)

    def __str__(self) -> str:
        return f"{self.path}"

    def __repr__(self) -> str:
        return f"Path({self.path})"

    def is_exists(self) -> bool:
        return os.path.exists(self.path)

class SyncCommand(BaseModel):
    command = CharField()

    @staticmethod
    def get_sync_command(args):
        sync_cmd, _ = SyncCommand.get_or_create(command=args)
        return sync_cmd

    def __str__(self) -> str:
        return self.command

class Source(BaseModel):
    label = CharField(unique=True)
    source = ForeignKeyField(Path)
    args = ForeignKeyField(SyncCommand)

    @staticmethod
    def is_exist(label) -> bool:
        return Source.select().where(Source.label == label).exists()

    @staticmethod
    def get_source(label):
        if not Source.is_exist(label):
            return None
        return Source.select().where(Source.label == label).get()

    @staticmethod
    def create_save(label:str, source:str, destinations:list[str], args:str):
        src_path, _ = Path.get_or_create(path=source)
        src_sync_cmd, _ = SyncCommand.get_or_create(command=args)
        src = Source.create(
            label=label,
            source=src_path,
            destinations=[],
            args=src_sync_cmd
        )
        for destination in destinations:
            des_path, _ = Path.get_or_create(path=destination)
            src_des, _ = Destination.get_or_create(source=src, path=des_path)
        src.save()
        return src

    def update_label(self, new_label):
        self.label = new_label
        self.save()

    def update_args(self, args):
        args_obj = SyncCommand.get_sync_command(args)
        self.args = args_obj
        self.save()

    def __str__(self) -> str:
        return f"{self.label}"

    def __repr__(self) -> str:
        return f"{self.label}"
class Destination(BaseModel):
    source = ForeignKeyField(Source, backref='destinations')
    path = ForeignKeyField(Path)

    def __str__(self) -> str:
        return f"{self.path}"

    @staticmethod
    def get_all(label:str|None = None):
        """
        Return all destiantions of the source.
        """
        if label is None:
            return []

        src = Source.get_source(label)
        if src is None:
            return []
        return src.destinations

class Group(BaseModel):
    label = CharField(unique=True)

    @staticmethod
    def is_exist(label) -> bool:
        return Group.select().where(Group.label == label).exists()

    @staticmethod
    def get_group(label):
        if not Group.is_exist(label):
            return None
        return Group.select().where(Group.label == label).get()

    @staticmethod
    def create_save(label:str, source_labels:list[str]):
        group = Group.create(
            label=label,
            sources=[],
        )

        GroupSource.create_group_sources(group, source_labels)
        group.save()
        return group

    def update_label(self, new_label):
        self.label = new_label
        self.save()

    def get_sources(self):
        """
        Return iterator of the group sources.
        """
        return (group_src.source for group_src in self.sources)

    def remove_sources(self):
        GroupSource.delete().where(GroupSource.group == self.label).execute()

    def __str__(self) -> str:
        return f"{self.label}"

    def __repl__(self) -> str:
        return f"{self.label}"

class GroupSource(BaseModel):
    group = ForeignKeyField(Group, backref='sources')
    source = ForeignKeyField(Source)

    @staticmethod
    def create_group_source(group:Group, source_label:str) -> bool:
        """
        Return group-source created status
        """
        src = Source.get(label=source_label)
        group_src, created = GroupSource.get_or_create(group=group, source=src)
        group_src.save()
        return created

    @staticmethod
    def create_group_sources(group:Group, source_labels:list[str]):
        for source_label in source_labels:
            GroupSource.create_group_source(group, source_label)

def create_tables():
    with db:
        tables = [
            Source,
            Path,
            Destination,
            SyncCommand,
            Group,
            GroupSource
        ]
        db.create_tables(tables, safe=True)

def all_group_labels():
    with db:
        return Group.select(Group.label)

def all_labels():
    with db:
        return Source.select(Source.label)

def all_labels_except(labels):
    if labels == None:
        return all_labels()
    if len(labels) == 0:
        return all_labels()
    with db:
        return Source.select(Source.label).where(Source.label.not_in(labels))

def count_all_labels_except(labels):
    return len(all_labels_except(labels))
