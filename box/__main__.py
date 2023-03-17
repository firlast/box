import sys
from os import path, mkdir
from typing import Union

from argeasy import ArgEasy

from .__init__ import __version__
from .tracker import Tracker
from .commit import Commit
from .ignore import get_non_ignored
from . import exceptions

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
    non_ignored = get_non_ignored()
    tracked = tracker.get_tracked()
    untracked = _get_untracked_files(non_ignored, tracked)

    if files == "*":
        files = untracked

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
    if not message:
        print('\033[1;31mA short message is required to commit\033[m')
        print('\033[33mUse "-m" flag and insert a message to commit\033[m')
        sys.exit(1)

    tracked = tracker.get_tracked()
    uncommitted = _get_uncommitted_files(tracked)

    try:
        if files == "*":
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

            commit_id = commit.commit(uncommitted, message)

        print(f'Commit #\033[4m{commit_id[:7]}\033[m "{message}"')
        print(f'\033[33m{len(files)} files committed\033[m')
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


def main() -> None:
    parser = ArgEasy(
        name='Box',
        description='Quick and simple file versioning with Box.',
        version=__version__
    )

    parser.add_argument('init', 'Init a empty repository', action='store_true')
    parser.add_argument('status', 'View uncommitted and untracked files', action='store_true')
    parser.add_argument('log', 'View commits log', action='store_true')
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
