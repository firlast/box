import os
import json
import pathlib

HOME_PATH = pathlib.Path.home()
BOX_CONFIG_PATH = os.path.join(HOME_PATH, '.box.config.json')


def _get_author() -> dict:
    try:
        with open(BOX_CONFIG_PATH, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        return {}
    else:
        return config.get('author')


def _set_author(name: str = None, email: str = None) -> None:
    author_info = _get_author()

    if name:
        author_info['name'] = name
    
    if email:
        author_info['email'] = email

    with open(BOX_CONFIG_PATH, 'w') as file:
        json.dump(author_info, file, indent=2)
