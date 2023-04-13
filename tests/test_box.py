import os
import sys
import json
import shutil
import marshal

import bupytest

sys.path.insert(0, './')

from box import tracker
from box import commit

REPO_DIR = '.box'
OBJECT_DIR = os.path.join(REPO_DIR, 'objects')
FILE_TESTS_DIR = os.path.join('tests', 'files')

if os.path.isdir(FILE_TESTS_DIR):
    shutil.rmtree(FILE_TESTS_DIR, ignore_errors=True)

if os.path.isdir(REPO_DIR):
    shutil.rmtree(REPO_DIR, ignore_errors=True)

os.mkdir(FILE_TESTS_DIR)
os.mkdir(REPO_DIR)
os.mkdir(OBJECT_DIR)

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


_tracker = tracker.Tracker()
_commit = commit.Commit()


class TestTracker(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

    def test_track(self):
        _tracker.track([TEST_FILE_1])
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
        _tracker.track([TEST_FILE_2])
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


class TestCommit(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

    def test_get_commits(self):
        commits = _commit.get_commits()
        self.assert_expected(commits, {})

    def test_commit(self):
        _tracker.update_track_info(TEST_FILE_1, committed=False)
        commit_id = _commit.commit('author', 'email', [TEST_FILE_1, TEST_FILE_2], message='first commit')
        commits = _commit.get_commits()

        self.assert_expected(len(commits), 1, message='Incorrect commits number')
        self.assert_true(commits.get(commit_id), message='Commit ID not found')
        self.assert_true(commits[commit_id]['message'], 'first commit')
        self.assert_expected(len(commits[commit_id]['objects']), 2, message='Expected 2 objects references')

        file_1_object_path = os.path.join(OBJECT_DIR, commits[commit_id]['objects'][TEST_FILE_1])
        file_2_object_path = os.path.join(OBJECT_DIR, commits[commit_id]['objects'][TEST_FILE_2])

        self.assert_true(
            value=os.path.isfile(file_1_object_path),
            message=f'Object to {repr(TEST_FILE_1)} not created'
        )

        self.assert_true(
            value=os.path.isfile(file_2_object_path),
            message=f'Object to {repr(TEST_FILE_2)} not created'
        )

    def test_commit_changed_file(self):
        with open(TEST_FILE_1, 'w') as file_1:
            file_1.write(TEST_FILE_1_CONTENT_CHANGED)

        with open(TEST_FILE_2, 'w') as file_2:
            file_2.write(TEST_FILE_2_CONTENT_CHANGED)

        commit_id = _commit.commit('author', 'email', [TEST_FILE_1, TEST_FILE_2], message='second commit')
        commits = _commit.get_commits()

        self.assert_expected(len(commits), 2, message='Incorrect commits number')
        self.assert_true(commits.get(commit_id), message='Commit ID not found')
        self.assert_true(commits[commit_id]['message'], 'second commit')
        self.assert_expected(len(commits[commit_id]['objects']), 2, message='Expected 1 object reference')

        file_1_object_path = os.path.join(OBJECT_DIR, commits[commit_id]['objects'][TEST_FILE_1])
        file_2_object_path = os.path.join(OBJECT_DIR, commits[commit_id]['objects'][TEST_FILE_2])

        self.assert_true(
            value=os.path.isfile(file_1_object_path),
            message=f'Object to {repr(TEST_FILE_1)} not created'
        )

        self.assert_true(
            value=os.path.isfile(file_2_object_path),
            message=f'Object to {repr(TEST_FILE_2)} not created'
        )

        with open(file_1_object_path, 'rb') as object_file:
            file_1_object_lines = marshal.load(object_file)

        with open(file_2_object_path, 'rb') as object_file:
            file_2_object_lines = marshal.load(object_file)

        self.assert_expected(
            value=file_1_object_lines,
            expected={
                1: 'This is a test!\n',
                2: 'A big test!'
            }
        )

        # "None" is a deleted line
        self.assert_expected(
            value=file_2_object_lines,
            expected={
                1: None
            }
        )


class TestIntegrity(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

    def test_check_integrity(self):
        self.assert_true(_commit.check_integrity())

    def test_external_change_object(self):
        commits = _commit.get_commits()
        last_commit = list(commits.values())[-1]
        commit_objects = last_commit['objects']

        file_1_object_id = commit_objects[TEST_FILE_1]
        file_1_object_path = os.path.join(OBJECT_DIR, file_1_object_id)

        with open(file_1_object_path, 'rb') as obj:
            original_content = obj.read()

        with open(file_1_object_path, 'wb') as obj:
            obj.write(b'changed content')

        self.assert_false(_commit.check_integrity())

        # rewrite original content to object
        with open(file_1_object_path, 'wb') as obj:
            obj.write(original_content)

    def test_commit_data_change_detect(self):
        commits = _commit.get_commits()
        last_commit = list(commits.keys())[-1]

        commits[last_commit]['author'] = 'Anonymous User'
        
        with open(os.path.join(REPO_DIR, 'commits.json'), 'w') as file:
            json.dump(commits, file)

        self.assert_false(_commit.check_integrity())
