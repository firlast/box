# Box, file versioning.
# Copyright (C) 2023  Firlast
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import json
from os import path
from hashlib import md5

from . import exceptions


class Tracker:
    def __init__(self) -> None:
        """
        Create a new instance from the Tracker class.
        """

        self._tracker_file = path.join('.box', 'tracker.json')

    @staticmethod
    def get_file_hash(filepath: str) -> str:
        with open(filepath, 'rb') as file:
            _hash = md5(file.read())

        return _hash.hexdigest()

    def dump_tracker(self, data: dict) -> None:
        with open(self._tracker_file, 'w') as tracker:
            json.dump(data, tracker, indent=2)

    def get_tracked(self) -> dict:
        """
        Get all tracked files.
        :return: Tracked files
        """

        try:
            with open(self._tracker_file) as tracker:
                tracked = json.load(tracker)
        except FileNotFoundError:
            tracked = {}

        return tracked

    def get_tracked_file(self, filepath: str) -> dict:
        tracked = self.get_tracked()
        try:
            file_tracked = tracked[filepath]
        except KeyError:
            raise exceptions.FileNotTrackedError(f'File {repr(filepath)} not tracked')

        return file_tracked

    def update_track_info(self, filepath: str, committed: bool, update_hash: bool = False) -> None:
        """
        Update `committed` status and file hash from
        tracked file.

        :param filepath: File path
        :param committed: File has committed
        :param update_hash: If true, this method update the
        file hash in tracked.
        :return:
        """

        tracked = self.get_tracked()

        if filepath in tracked:
            if update_hash:
                tracked[filepath]['hash'] = self.get_file_hash(filepath)
            tracked[filepath]['committed'] = committed
            self.dump_tracker(tracked)
        else:
            raise exceptions.FileNotTrackedError(f'File "{filepath}" not tracked')

    def track(self, files_list: list) -> None:
        """
        Track a new files.

        This method generate a hash from file and add
        this information to a tracker file specified in
        `self._tracker_file`.

        :param files_list: Files path to track
        :return: None
        """

        tracked = self.get_tracked()

        for filepath in files_list:
            try:
                with open(filepath) as _test_file:
                    _test_file.read()
            except UnicodeDecodeError:
                binary = True
            else:
                binary = False

            file_hash = self.get_file_hash(filepath)
            tracked[filepath] = dict(hash=file_hash, committed=False, binary=binary)

        self.dump_tracker(tracked)
