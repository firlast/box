from argeasy import ArgEasy
from .__init__ import __version__


def main() -> None:
    parser = ArgEasy(
        name='Box',
        description='Quick and simple file versioning with Box.',
        version=__version__
    )

    parser.add_argument('init', 'Init a empty repository', action='store_true')
