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
import marshal
from hashlib import md5
from os import path
from typing import List
from datetime import datetime

from .tracker import Tracker
from . import exceptions
from . import utils


class Commit:
    def __init__(self, repo_path: str) -> None:
        """
        This class handles everything about `commits`.
        :param repo_path: Repository path
        """

        self._commit_file = path.join(repo_path, 'commits.json')
        self._obj_file = path.join(repo_path, 'objects')
        self._tracker = Tracker(repo_path)

        self._commits = self._get_commits()

    def _dump_commit_file(self, data: dict) -> None:
        with open(self._commit_file, 'w') as file:
            json.dump(data, file, indent=2)

    def _create_object(self, file_diff: dict, obj_id: str) -> None:
        object_path = path.join(self._obj_file, obj_id)

        with open(object_path, 'wb') as _object:
            marshal.dump(file_diff, _object)

    def _create_object_to_binary(self, file_content: bytes, obj_id: str) -> None:
        object_path = path.join(self._obj_file, obj_id)

        with open(object_path, 'wb') as _object:
            _object.write(file_content)

    def _get_object(self, object_id: str) -> dict:
        object_path = path.join(self._obj_file, object_id)
        with open(object_path, 'rb') as file:
            object_data = marshal.load(file)

        return object_data

    def _get_object_hash(self, object_id: str) -> bytes:
        object_path = path.join(self._obj_file, object_id)
        with open(object_path, 'rb') as file:
            _hash = md5(file.read())

        return _hash.digest()

    def _get_file_commits(self, filename: str) -> dict:
        commits = self.get_commits()
        file_commits = {cid: cdata for cid, cdata in commits.items() if filename in cdata['objects']}
        return file_commits

    def _get_commits(self) -> dict:
        try:
            with open(self._commit_file, 'rb') as file:
                commits = json.load(file)
        except FileNotFoundError:
            commits = {}

        return commits

    def _get_commit_hash(self, commit_id: str) -> bytes:
        commits = self.get_commits()
        commit: dict = commits[commit_id].copy()

        objects_hashes = [self._get_object_hash(obj) for obj in commit.pop('objects').values()]
        objects_sum_hash = md5(b''.join(objects_hashes)).hexdigest()
        commit_info = '.'.join([commit_id, objects_sum_hash, *commit.values()])
        _hash = md5(commit_info.encode()).hexdigest()

        return _hash

    def _get_last_commit_hash(self) -> str:
        commits = self.get_commits()

        if commits:
            commit_id = list(commits.keys())[-1]
            _hash = self._get_commit_hash(commit_id)
        else:
            _hash = ''

        return _hash

    def get_commits(self, until_commit_id: str = None) -> dict:
        """
        Get all commits in `dict` format. The commit
        data contains commit datetime, message and
        objects references.

        :param until_commit_id: Get all commits until a commit ID.
        :return: Commits
        """

        if until_commit_id:
            filtered_commits = {}
            for cid, cdata in self._commits.items():
                if cid != until_commit_id:
                    filtered_commits[cid] = cdata
                else:
                    filtered_commits[cid] = cdata
                    break

            return filtered_commits

        return self._commits

    def merge_objects(self, file: str) -> dict:
        file_commits = self._get_file_commits(file)
        file_objects = [self._get_object(commit['objects'][file]) for commit in file_commits.values()]
        merged = {}

        for file_obj in file_objects:
            merged.update(file_obj)

        return merged

    def _create_commit_objects(self, files: list, commit_id: str) -> dict:
        tracked = self._tracker.get_tracked()
        commit_objects = {}

        # check if all files are tracked
        for file in files:
            if file not in tracked:
                raise exceptions.FileNotTrackedError(f'File "{file}" not tracked')

        for file in files:
            obj_id = utils.generate_id(commit_id, file)
            commit_objects[file] = obj_id
            file_info = tracked[file]

            if file_info['binary']:
                current_hash = self._tracker.get_file_hash(file)
                tracked[file]['hash'] = current_hash
                with open(file, 'rb') as file_r:
                    file_content = file_r.read()

                if file_info['committed']:
                    if tracked[file]['hash'] != current_hash:
                        self._create_object_to_binary(file_content, obj_id)
                else:
                    tracked[file]['committed'] = True
                    self._create_object_to_binary(file_content, obj_id)
            else:
                with open(file, 'r') as file_r:
                    file_lines = utils.enumerate_lines(file_r.readlines())

                if not file_info['committed']:
                    tracked[file]['committed'] = True
                else:
                    current_hash = self._tracker.get_file_hash(file)

                    if file_info['hash'] != current_hash:
                        merged = self.merge_objects(file)
                        tracked[file]['hash'] = current_hash
                        file_lines = utils.difference_lines(merged, file_lines)

                self._create_object(file_lines, obj_id)

        self._tracker.dump_tracker(tracked)
        return commit_objects

    def commit(self, author: str, author_email: str, files: List[str], message: str) -> str:
        """Commit files with a message.

        If is the first file commit, this method enumerate
        all file lines and store this in an "object", the
        object ID is stored in commit data. Otherwise, this method
        gets the difference of all merged file commits from
        enumerate file lines and store this difference.

        :param author: Author name
        :type author: str
        :param author_email: Author email
        :type author_email: str
        :param files: Files to commit
        :type files: List[str]
        :param message: Message to describe changes
        :type message: str
        :raises exceptions.NoFilesToCommitError: If no file has changed
        :return: Return commit ID
        :rtype: str
        """

        commits = self.get_commits()

        commit_datetime = str(datetime.now().replace(microsecond=0))
        commit_id = utils.generate_id(commit_datetime, message)
        commit_objects = self._create_commit_objects(files, commit_id)

        if not commit_objects:
            raise exceptions.NoFilesToCommitError('No files to commit')

        commits[commit_id] = dict(
            author=author,
            author_email=author_email,
            message=message,
            date=str(commit_datetime),
            objects=commit_objects,
            phash=self._get_last_commit_hash()
        )

        self._commits = commits
        self._dump_commit_file(commits)
        return commit_id

    def check_integrity(self) -> bool:
        """Check commits integrity.

        If any commit is altered by a third party, `False` is
        returned, indicating that the commit chain is invalid.

        :return: If chain is valid
        :rtype: bool
        """

        commits = self.get_commits()
        last_hash = ''

        for commit_id in commits.keys():
            if commits[commit_id]['phash'] == last_hash:
                last_hash = self._get_commit_hash(commit_id)
            else:
                return False
        
        return True
