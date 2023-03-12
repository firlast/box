import hashlib
import json

from . import exceptions


class Tracker:
    def __init__(self, tracker_filepath: str) -> None:
        self._tracker_file = tracker_filepath

    @staticmethod
    def _get_file_hash(filepath: str) -> str:
        with open(filepath, 'rb') as file:
            _hash = hashlib.md5(file.read())

        return _hash.hexdigest()

    def _dump_tracker(self, data: dict) -> None:
        with open(self._tracker_file, 'w') as tracker:
            json.dump(data, tracker, indent=2)

    def get_tracked(self) -> dict:
        try:
            with open(self._tracker_file) as tracker:
                tracked = json.load(tracker)
        except FileNotFoundError:
            tracked = {}

        return tracked

    def update_committed_status(self, filepath: str, committed: bool) -> None:
        tracked = self.get_tracked()

        if filepath in tracked:
            tracked[filepath]['committed'] = committed
        else:
            raise exceptions.FileNotTrackedError(f'File "{filepath}" not tracked')

    def track(self, filepath: str) -> None:
        tracked = self.get_tracked()

        if filepath in tracked:
            raise exceptions.FileAlreadyTrackedError(f'File "{filepath}" already tracked')
        else:
            file_hash = self._get_file_hash(filepath)
            tracked[filepath] = {
                'hash': file_hash,
                'committed': False
            }

            self._dump_tracker(tracked)
