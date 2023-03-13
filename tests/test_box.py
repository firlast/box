import os
import sys

import bupytest
import box

FILE_TESTS_DIR = os.path.join(os.getcwd(), 'files')
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
