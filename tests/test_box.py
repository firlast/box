import os
import sys

import bupytest
from box import tracker
from box import commit

FILE_TESTS_DIR = os.path.join(os.getcwd(), 'files')
REPO_DIR = os.path.join(os.getcwd(), '.box')

if not os.path.isdir(FILE_TESTS_DIR):
    os.mkdir(FILE_TESTS_DIR)

if not os.path.isdir(REPO_DIR):
    os.mkdir(REPO_DIR)

TEST_FILE_1 = os.path.join(FILE_TESTS_DIR, 'readme.md')
TEST_FILE_2 = os.path.join(FILE_TESTS_DIR, 'hello.txt')

TEST_FILE_1_CONTENT = (
    '# Box Version Control Test\n'
    'This is a test!'
)

TEST_FILE_1_CONTENT_CHANGED = (
    '# Box Version Control Test\n'
    'This is a test!\n',
    'A big test!'
)

TEST_FILE_2_CONTENT = (
    'Hello Word!\n',
    'How are you?'
)

TEST_FILE_2_CONTENT_CHANGED = (
    'Hello Word!\n',
)

if __name__ == '__main__':
    bupytest.this()
