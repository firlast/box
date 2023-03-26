# Box, file versioning.
# Copyright (C) 2023  Firlast
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import time
from os import path, mkdir
from typing import Union

from argeasy import ArgEasy

from .__init__ import __version__
from .tracker import Tracker
from .commit import Commit
from .ignore import get_non_ignored
from . import _config
from . import exceptions
from . import utils

REPO_PATH = '.box'
OBJECTS_PATH = path.join(REPO_PATH, 'objects')

tracker = Tracker(REPO_PATH)
commit = Commit(REPO_PATH)


def _get_uncommitted_files(tracked: dict) -> list:
    return [filepath for filepath, info in tracked.items() if not info['committed']]


def _get_untracked_files(non_ignored: list, tracked: dict) -> list:
    return [file for file in non_ignored if file not in tracked]


def _init() -> None:
    if path.isdir(REPO_PATH):
        print(f'\033[33mRepository already started in {repr(REPO_PATH)}\033[m')
        sys.exit(1)
    else:
        mkdir(REPO_PATH)
        mkdir(OBJECTS_PATH)
        print(f'\033[32mNew repository started in {repr(REPO_PATH)}\033[m')


def _add(files: Union[list, str]) -> None:
    if files == "*":
        non_ignored = get_non_ignored()
        tracked = tracker.get_tracked()
        files = _get_untracked_files(non_ignored, tracked)

    for file in files:
        if not path.isfile(file):
            print(f'\033[31mFile {repr(file)} not exists in current directory\033[m')
            sys.exit(1)

    tracker.track(files)


def _status() -> None:
    non_ignored = get_non_ignored()
    tracked_files = tracker.get_tracked()

    uncommitted = _get_uncommitted_files(tracked_files)
    untracked = _get_untracked_files(non_ignored, tracked_files)

    if uncommitted or untracked:
        print('\033[1mUncommitted files\033[m')

        if uncommitted:
            print(f'Use "commit" argument to commit {len(uncommitted)} files:\033[33m')
            for file in uncommitted:
                print('   ' + file)
        else:
            print('0 files found for commit')

        print('\n\033[37;1mUntracked files\033[m')

        if untracked:
            print(f'Use "add" argument to track {len(untracked)} files:\033[33m')
            for file in untracked:
                print('   ' + file)
        else:
            print('0 files found for tracking')

        print('\033[m')
    else:
        print('\033[1mDirectory without new files or changes!\033[m')
        print('\033[33m0 files found for track or commit\033[m')


def _commit(files: Union[list, str], message: str) -> None:
    author = _config.get_author()

    if not author:
        print('\033[1;31mPlease set the author\'s name and email before\033[m')
        print('\033[33mUse "config" command to set author information\033[m')
        print('Example: \033[4mbox config --name "Name" --email "Email"\033[m')

    if not message:
        print('\033[1;31mA short message is required to commit\033[m')
        print('\033[33mUse "-m" flag and insert a message to commit\033[m')
        sys.exit(1)

    tracked = tracker.get_tracked()
    uncommitted = _get_uncommitted_files(tracked)

    try:
        if files == "*":
            time_s = time.time()
            commit_id = commit.commit(uncommitted, message)
            files = uncommitted
        else:
            for file in files:
                if not path.isfile(file):
                    print(f'\033[1;31mFile {repr(file)} dont\'t exists\033[m')
                    sys.exit(1)
                elif file not in tracked:
                    print(f'\033[1;31mFile {repr(file)} not tracked for commit\033[m')
                    print('\033[33mUse "add" argument to track this file\033[m')
                    sys.exit(1)

            time_s = time.time()
            commit_id = commit.commit(files, message)

        print(f'Commit #\033[4m{commit_id[:7]}\033[m "{message}"')
        print(f'\033[33m{len(files)} files committed in {time.time() - time_s:.3f}s\033[m')
    except exceptions.NoFilesToCommitError:
        print('\033[1;31mNo files changed to commit\033[m')
        print('\033[33mYou can only commit changed and tracked files\033[m')


def _log() -> None:
    commits = commit.get_commits()

    for cid, cdata in reversed(commits.items()):
        message = cdata['message']
        date = cdata['date']
        files = len(cdata['objects'])
        print(f'{files} files committed in \033[34;4m{cid[:7]}\033[m: ({date}) \033[33m{repr(message)}\033[m')


def _diff() -> None:
    tracked = tracker.get_tracked()

    for file, info in tracked.items():
        if not info['binary']:
            with open(file, 'r') as reader:
                content = reader.readlines()

            merged = commit.merge_objects(file)
            current_lines = utils.enumerate_lines(content)
            diff = utils.difference_lines(merged, current_lines)
            
            if diff:
                print(f'\033[1mfile {repr(file)} diff\033[m')
                print(f'\033[33m{len(diff)} lines changed\n\033[m')

                for number, line in diff.items():
                    if line is None:
                        print(f'    \033[31m{number} | -- {merged[number]}\033[m')
                    else:
                        print(f'    \033[32m{number} | ++ {line}\033[m')

                print()
        else:
            print('\033[1;31mCannot get difference of binary files\033[m')
            sys.exit(1)


def _integrity():
    if commit.check_integrity():
        print('\033[1;32mCommits without external changes\033[m')
        print(f'\033[33m{len(commit.get_commits())} commits checked\033[m')
    else:
        print('\033[1;31mSome commits were changed inappropriately\033[m')
        print(f'\033[33m{len(commit.get_commits())} files checked\033[m')


def main() -> None:
    if not path.isfile(OBJECTS_PATH):
        print('\033[1;31mRepository not found\033[m')
        print('\033[33mCreate a repository with "init" command\033[m')
        sys.exit(1)

    parser = ArgEasy(
        name='Box',
        description='Quick and simple file versioning with Box.',
        version=__version__
    )

    parser.add_argument('init', 'Init a empty repository', action='store_true')
    parser.add_argument('status', 'View uncommitted and untracked files', action='store_true')
    parser.add_argument('log', 'View commits log', action='store_true')
    parser.add_argument('diff', 'Get difference of files', action='store_true')
    parser.add_argument('integrity', 'Check commits integrity', action='store_true')
    parser.add_argument('add', 'Add new files to track list', action='append')
    parser.add_argument('commit', 'Commit files', action='append')

    parser.add_flag('-a', 'Select all files to tracking', action='store_true')
    parser.add_flag('-am', 'Commit all changed files add insert a message')
    parser.add_flag('-m', 'A short message to commit')

    args = parser.parse()

    if args.init:
        _init()
    elif args.add is not None:
        if args.a:
            _add('*')
        else:
            _add(args.add)
    elif args.status:
        _status()
    elif args.log:
        _log()
    elif args.commit is not None:
        if args.am:
            _commit('*', args.am)
        else:
            _commit(args.commit, args.m)
    elif args.diff:
        _diff()
    elif args.integrity:
        _integrity()
