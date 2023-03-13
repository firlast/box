import os
import json
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

    def _create_object(self, file_diff: dict, obj_id: str) -> None:
        object_path = os.path.join(self._obj_file, obj_id)

        with open(object_path, 'w') as _object:
            json.dump(file_diff, _object, separators=(',', ':'))

    def _get_object(self, object_id: str) -> dict:
        object_path = os.path.join(self._obj_file, object_id)
        with open(object_path, 'rb') as file:
            object_data = json.load(file)

        return object_data

    def _get_file_commits(self, filename: str) -> dict:
        commits = self.get_commits()
        file_commits = {cid: cdata for cid, cdata in commits.items() if filename in cdata['objects']}
        return file_commits

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
        commit_datetime = str(datetime.now().replace(microsecond=0))
        commit_id = utils.generate_id(commit_datetime, message)

        for file in files:
            if not tracked[file]['committed']:
                with open(file, 'r') as file_r:
                    file_lines = utils.enumerate_lines(file_r.readlines())

                self._tracker.update_track_info(committed=True)

            obj_id = utils.generate_id(commit_datetime, message, file)
            commit_objects[file] = obj_id
            self._create_object(file_lines, obj_id)

        commits[commit_id] = dict(
            message=message,
            date=str(commit_datetime),
            objects=object,
        )

        self._dump_commit_file(commits)
        return commit_id
