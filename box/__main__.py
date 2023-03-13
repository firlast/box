import os
import sys

from argeasy import ArgEasy

from .__init__ import __version__
from .tracker import Tracker
from .commit import Commit

REPO_PATH = os.path.join('./', '.box')
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


def main() -> None:
    parser = ArgEasy(
        name='Box',
        description='Quick and simple file versioning with Box.',
        version=__version__
    )

    parser.add_argument('init', 'Init a empty repository', action='store_true')
    parser.add_argument('add', 'Add new files to track list', action='append')
    args = parser.parse()

    if args.init:
        init()
    elif args.add:
        add(args.add)
