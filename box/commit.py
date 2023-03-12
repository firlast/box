import json


class Commit:
    def __init__(self, commit_filepath: str) -> None:
        self._commit_file = commit_filepath

    def _dump_commit_file(self, data: dict) -> None:
        with open(self._commit_file, 'w') as file:
            json.dump(data, file, indent=2)
