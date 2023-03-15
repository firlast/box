import os
import sys

from argeasy import ArgEasy

from .__init__ import __version__
from .tracker import Tracker
from .commit import Commit
from .ignore import get_non_ignored

REPO_PATH = '.box'
OBJECTS_PATH = os.path.join(REPO_PATH, 'objects')

tracker = Tracker(REPO_PATH)
commit = Commit(REPO_PATH)


def init() -> None:
    if os.path.isdir(REPO_PATH):
        print(f'\033[33mRepository already started in {repr(REPO_PATH)}\033[m')
        sys.exit(1)
    else:
        os.mkdir(REPO_PATH)
        os.mkdir(OBJECTS_PATH)
        print(f'\033[32mNew repository started in {repr(REPO_PATH)}\033[m')


def add(files: list) -> None:
    for file in files:
        if not os.path.isfile(file):
            print(f'\033[31mFile {repr(file)} not exists in current directory\033[m')
            sys.exit(1)

    tracker.track(files)


def status() -> None:
    non_ignored = get_non_ignored()
    tracked_files = tracker.get_tracked()

    uncommitted = [filepath for filepath, info in tracked_files.items() if not info['committed']]
    untracked = [file for file in non_ignored if file not in tracked_files]

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


def main() -> None:
    parser = ArgEasy(
        name='Box',
        description='Quick and simple file versioning with Box.',
        version=__version__
    )

    parser.add_argument('init', 'Init a empty repository', action='store_true')
    parser.add_argument('add', 'Add new files to track list', action='append')
    parser.add_argument('status', 'View uncommitted and untracked files', action='store_true')
    args = parser.parse()

    if args.init:
        init()
    elif args.add:
        add(args.add)
    elif args.status:
        status()
