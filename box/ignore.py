import os


def _filter_filelist(path: str) -> str:
    if path.startswith('/'):
        path = path[1:]

    return os.path.abspath(path)


def _path_has_ignored(ignored: list, path: str) -> bool:
    for i in ignored:
        if i in os.path.abspath(path):
            return True


def _load_ignore() -> list:
    try:
        with open('.ignore', 'r') as ignore_file:
            filelist = ignore_file.readlines()
    except FileNotFoundError:
        ignored = []
    else:
        filelist = [file.replace('\n', '') for file in filelist]
        ignored = list(map(_filter_filelist, filelist))

    ignored.append('.box')
    return ignored


def get_non_ignored() -> list:
    ignored = _load_ignore()
    non_ignored = []

    for root, dirs, files in os.walk('.'):
        if not _path_has_ignored(ignored, root):
            for file in files:
                filepath = os.path.join(root, file)
                if not _path_has_ignored(ignored, filepath):
                    non_ignored.append(filepath.replace('./', ''))

    return non_ignored
