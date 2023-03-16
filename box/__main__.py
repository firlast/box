import os
import sys
from typing import Union

from argeasy import ArgEasy

from .__init__ import __version__
from .tracker import Tracker
from .commit import Commit
from .ignore import get_non_ignored

REPO_PATH = '.box'
OBJECTS_PATH = os.path.join(REPO_PATH, 'objects')

tracker = Tracker(REPO_PATH)
commit = Commit(REPO_PATH)


def _get_uncommitted_files(tracked: dict) -> list:
    return [filepath for filepath, info in tracked.items() if not info['committed']]


def _get_untracked_files(non_ignored: list, tracked: dict) -> list:
    return [file for file in non_ignored if file not in tracked]


def _init() -> None:
    if os.path.isdir(REPO_PATH):
        print(f'\033[33mRepository already started in {repr(REPO_PATH)}\033[m')
        sys.exit(1)
    else:
        os.mkdir(REPO_PATH)
        os.mkdir(OBJECTS_PATH)
        print(f'\033[32mNew repository started in {repr(REPO_PATH)}\033[m')


def _add(files: list) -> None:
    for file in files:
        if not os.path.isfile(file):
            print(f'\033[31mFile {repr(file)} not exists in current directory\033[m')
            sys.exit(1)

    tracker.track(files)


def _status() -> None:
    non_ignored = get_non_ignored()
    tracked_files = tracker.get_tracked()

    uncommitted = _get_uncommitted_files(tracked_files)
    untracked = _get_untracked_files(non_ignored, tracked_files)

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


def _commit(files: Union[list, str], message: str) -> None:
    if not message:
        print('\033[1;31mA short message is required to commit\033[m')
        print('\033[33mUse "-m" flag and insert a message to commit\033[m')
        sys.exit(1)

    tracked = tracker.get_tracked()
    uncommitted = _get_uncommitted_files(tracked)

    if files == "*":
        commit_id = commit.commit(uncommitted, message)
        files = tracked.keys()
    else:
        for file in files:
            if not os.path.isfile(file):
                print(f'\033[1;31mFile {repr(file)} not tracked for commit\033[m')
                print('\033[33mUse "add" argument to track this file\033[m')
                sys.exit(1)
            elif file not in tracked:
                print(f'\033[1;31mFile {repr(file)} not tracked for commit\033[m')
                print('\033[33mUse "add" argument to track this file\033[m')
                sys.exit(1)

        commit_id = commit.commit(uncommitted, message)

    print(f'Commit #\033[4m{commit_id[:7]}\033[m "{message}"')
    print(f'\033[33m{len(files)} files committed\033[m')


def main() -> None:
    parser = ArgEasy(
        name='Box',
        description='Quick and simple file versioning with Box.',
        version=__version__
    )

    parser.add_argument('init', 'Init a empty repository', action='store_true')
    parser.add_argument('status', 'View uncommitted and untracked files', action='store_true')
    parser.add_argument('add', 'Add new files to track list', action='append')
    parser.add_argument('commit', 'Commit files', action='append')

    parser.add_flag('-am', 'Commit all changed files add insert a message')
    parser.add_flag('-m', 'A short message to commit')

    args = parser.parse()

    if args.init:
        _init()
    elif args.add:
        _add(args.add)
    elif args.status:
        _status()
    elif args.commit is not None:
        if args.am:
            _commit('*', args.am)
        else:
            _commit(args.commit, args.m)
