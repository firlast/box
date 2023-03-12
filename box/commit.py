import os
import json
import secrets


class Commit:
    def __init__(self, repo_path: str) -> None:
        self._commit_file = os.path.join(repo_path, 'commits.json')
        self._obj_file = os.path.join(repo_path, 'objects')

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
