import hashlib
import json


class Tracker:
    def __init__(self, tracker_filepath: str) -> None:
        self._tracker_file = tracker_filepath

    @staticmethod
    def _get_file_hash(filepath: str) -> str:
        with open(filepath, 'rb') as file:
            _hash = hashlib.md5(file.read())

        return _hash.hexdigest()

    def get_tracked(self) -> dict:
        try:
            with open(self._tracker_file) as tracker:
                tracked = json.load(tracker)
        except FileNotFoundError:
            tracked = {}

        return tracked
