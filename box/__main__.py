import os
import sys

from argeasy import ArgEasy
from .__init__ import __version__

REPO_PATH = os.path.join('./', '.box')
OBJECTS_PATH = os.path.join(REPO_PATH, 'objects')


def init() -> None:
    if os.path.isdir(REPO_PATH):
        print(f'\033[33mRepository already started in {repr(REPO_PATH)}\033[m')
        sys.exit(1)
    else:
        os.mkdir(REPO_PATH)
        os.mkdir(OBJECTS_PATH)
        print(f'\033[32mNew repository started in {repr(REPO_PATH)}\033[m')


def main() -> None:
    parser = ArgEasy(
        name='Box',
        description='Quick and simple file versioning with Box.',
        version=__version__
    )

    parser.add_argument('init', 'Init a empty repository', action='store_true')
    args = parser.parse()

    if args.init:
        init()
