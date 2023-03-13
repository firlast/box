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


class TestTracker(bupytest.UnitTest):
    def __init__(self):
        super().__init__()
        self.tracker = tracker.Tracker(REPO_DIR)

    def test_track(self):
        self.tracker.track(TEST_FILE_1)
        tracked = self.tracker.get_tracked()

        self.assert_true(TEST_FILE_1 in tracked, message='File not found in tracked data')
        self.assert_expected(
            value=tracked[TEST_FILE_1]['committed'],
            expected=False,
            message='File not found in tracked data'
        )


if __name__ == '__main__':
    bupytest.this()
