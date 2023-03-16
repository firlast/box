import os
import json
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
        """
        Get all commits in `dict` format. The commit
        data contains commit datetime, message and
        objects references.

        :param until_commit_id: Get all commits until a commit ID.
        :return: Commits
        """

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
        """
        Commit files with a message.

        If is the first file commit, this method enumerate
        all file lines and store this in an "object", the
        object ID is stored in commit data. Otherwise, this method
        gets the difference of all merged file commits from
        enumerate file lines and store this difference.

        :param files: Files to commit
        :param message: A message to describe this change
        :return: Commit ID
        """

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
            with open(file, 'r') as file_r:
                file_lines = utils.enumerate_lines(file_r.readlines())

            if not tracked[file]['committed']:
                self._tracker.update_track_info(file, committed=True)
            elif self._tracker.get_tracked_file(file)['hash'] != self._tracker.get_file_hash(file):
                file_commits = self._get_file_commits(file)
                file_objects = [commit['objects'][file] for commit in file_commits.values()]
                merged_lines = {}

                for obj_id in file_objects:
                    merged_lines.update(self._get_object(obj_id))

                self._tracker.update_track_info(file, committed=True, update_hash=True)
                file_lines = utils.difference_lines(merged_lines, file_lines)
            else:
                # ignore files without changes
                continue

            obj_id = utils.generate_id(commit_id, file)
            commit_objects[file] = obj_id
            self._create_object(file_lines, obj_id)

        if not commit_objects:
            raise exceptions.NoFilesToCommitError('No files to commit')

        commits[commit_id] = dict(
            message=message,
            date=str(commit_datetime),
            objects=commit_objects,
        )

        self._dump_commit_file(commits)
        return commit_id
