import os
import json
import secrets
import hashlib
from typing import List
from datetime import datetime

from .tracker import Tracker
from . import exceptions
from . import utils


class Commit:
    def __init__(self, repo_path: str) -> None:
        self._commit_file = os.path.join(repo_path, 'commits.json')
        self._obj_file = os.path.join(repo_path, 'objects')
        self._tracker = Tracker(repo_path)

    def _dump_commit_file(self, data: dict) -> None:
        with open(self._commit_file, 'w') as file:
            json.dump(data, file, indent=2)

    def _create_object(self, file_diff: dict) -> str:
        object_id = secrets.token_hex(32)
        object_path = os.path.join(self._obj_file, object_id)

        with open(object_path, 'w') as _object:
            json.dump(file_diff, _object, separators=(',', ':'))

        return object_id

    def get_commits(self, until_commit_id: str = None) -> dict:
        try:
            with open(self._commit_file, 'rb') as file:
                commits = json.load(file)
        except FileNotFoundError:
            commits = {}

        if until_commit_id:
            filtered_commits = {}

            for cid, cdata in commits.items():
                if cid != until_commit_id:
                    filtered_commits[cid] = cdata
                else:
                    break

            return filtered_commits

        return commits

    def commit(self, files: List[str], message: str) -> str:
        tracked = self._tracker.get_tracked()
        commits = self.get_commits()

        # check if all files are tracked
        for file in files:
            if file not in tracked:
                raise exceptions.FileNotTrackedError(f'File "{file}" not tracked')

        commit_objects = {}

        for file in files:
            if not tracked[file]['committed']:
                with open(file, 'r') as file_r:
                    file_enum_lines = utils.enumerate_lines(file_r.readlines())

                obj_id = self._create_object(file_enum_lines)
                commit_objects[file] = obj_id

        commit_datetime = str(datetime.now().replace(microsecond=0))
        id_parts = ''.join((
            secrets.token_hex(16),
            message,
            commit_datetime
        ))

        commit_id = hashlib.sha1(id_parts.encode()).hexdigest()

        commits[commit_id] = dict(
            message=message,
            date=str(commit_datetime),
            objects=object,
        )

        self._dump_commit_file(commits)
