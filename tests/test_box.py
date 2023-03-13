import os
import shutil

import bupytest
from box import tracker

FILE_TESTS_DIR = os.path.join(os.getcwd(), 'files')
REPO_DIR = os.path.join(os.getcwd(), '.box')

if os.path.isdir(FILE_TESTS_DIR):
    shutil.rmtree(FILE_TESTS_DIR, ignore_errors=True)

if os.path.isdir(REPO_DIR):
    shutil.rmtree(REPO_DIR, ignore_errors=True)

os.mkdir(FILE_TESTS_DIR)
os.mkdir(REPO_DIR)

TEST_FILE_1 = os.path.join(FILE_TESTS_DIR, 'readme.md')
TEST_FILE_2 = os.path.join(FILE_TESTS_DIR, 'hello.txt')

TEST_FILE_1_CONTENT = (
    '# Box Version Control Test\n'
    'This is a test!'
)

TEST_FILE_1_CONTENT_CHANGED = (
    '# Box Version Control Test\n'
    'This is a test!\n'
    'A big test!'
)

TEST_FILE_2_CONTENT = (
    'Hello Word!\n'
    'How are you?'
)

TEST_FILE_2_CONTENT_CHANGED = (
    'Hello Word!\n'
)

with open(TEST_FILE_1, 'w') as file:
    file.write(TEST_FILE_1_CONTENT)

with open(TEST_FILE_2, 'w') as file:
    file.write(TEST_FILE_2_CONTENT)


_tracker = tracker.Tracker(REPO_DIR)


class TestTracker(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

    def test_track(self):
        _tracker.track(TEST_FILE_1)
        tracked = _tracker.get_tracked()

        self.assert_true(len(tracked) == 1, message='Tracked data larger than necessary')
        self.assert_true(tracked.get(TEST_FILE_1), message='File not found in tracked data')
        self.assert_expected(
            value=tracked[TEST_FILE_1]['committed'],
            expected=False,
            message='Committed status is not False'
        )

        self._tracked_file_hash = tracked[TEST_FILE_1]['hash']
        self._tracked_file_committed = tracked[TEST_FILE_1]['committed']

    def test_track_other_file(self):
        _tracker.track(TEST_FILE_2)
        tracked = _tracker.get_tracked()

        self.assert_true(len(tracked) == 2, message='Tracked data larger (or smaller) than necessary')
        self.assert_true(tracked.get(TEST_FILE_2), message='File not found in tracked data')
        self.assert_expected(
            value=tracked[TEST_FILE_2]['committed'],
            expected=False,
            message='Committed status is not False'
        )

    def test_update_committed_status(self):
        _tracker.update_track_info(TEST_FILE_1, committed=True)
        tracked = _tracker.get_tracked()

        self.assert_expected(
            value=tracked[TEST_FILE_1]['hash'],
            expected=self._tracked_file_hash,
            message='Hash updated unnecessarily'
        )

        self.assert_expected(
            value=tracked[TEST_FILE_1]['committed'],
            expected=True,
            message='Committed status not updated'
        )


if __name__ == '__main__':
    bupytest.this()
