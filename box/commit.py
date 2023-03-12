import json


class Commit:
    def __init__(self, commit_filepath: str) -> None:
        self._commit_file = commit_filepath

    def _dump_commit_file(self, data: dict) -> None:
        with open(self._commit_file, 'w') as file:
            json.dump(data, file, indent=2)

    def get_commits(self, until_commit_id: str = None) -> dict:
        with open(self._commit_file, 'rb') as file:
            commits = json.load(file)

        if until_commit_id:
            filtered_commits = {}

            for cid, cdata in commits:
                if cid != until_commit_id:
                    filtered_commits[cid] = cdata
                else:
                    break

            return filtered_commits

        return commits
