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
