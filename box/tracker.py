import hashlib
import json

from . import exceptions


class Tracker:
    def __init__(self, tracker_filepath: str) -> None:
        """
        Create a new instance from the Tracker class.
        :param tracker_filepath: A JSON file path
        """

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

    def update_track_info(self, filepath: str, committed: bool) -> None:
        """
        Update `committed` status and file hash from
        tracked file.

        :param filepath: File path
        :param committed: File has committed
        :return: None
        """

        tracked = self.get_tracked()

        if filepath in tracked:
            tracked[filepath]['hash'] = self._get_file_hash(filepath)
            tracked[filepath]['committed'] = committed
            self._dump_tracker(tracked)
        else:
            raise exceptions.FileNotTrackedError(f'File "{filepath}" not tracked')

    def track(self, filepath: str) -> None:
        """
        Track a new file.

        This method generate a hash from file and add
        this information to a tracker file specified in
        `self._tracker_file`.

        :param filepath: File path to track
        :return: None
        """

        tracked = self.get_tracked()

        if filepath in tracked:
            raise exceptions.FileAlreadyTrackedError(f'File "{filepath}" already tracked')
        else:
            file_hash = self._get_file_hash(filepath)
            tracked[filepath] = dict(hash=file_hash, committed=False)
            self._dump_tracker(tracked)
