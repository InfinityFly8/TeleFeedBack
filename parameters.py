import logging
import json
from contextlib import suppress
from types import SimpleNamespace
import emoji

#logging init
logger = logging.getLogger('feedback bot')
logger.setLevel(logging.INFO)

logging.basicConfig()
settings_logger = logging.getLogger('settings_log')
settings_logger.setLevel(logging.WARN)


def dict_to_object(dict_: dict):
    '''converts dict to object with recursion'''
    obj = {}
    for key, value in dict_.items():
        if isinstance(value, dict):
            value = dict_to_object(value)
        if isinstance(value, str):
            value = emoji.emojize(value, use_aliases=True)
        obj[key] = value
    return SimpleNamespace(**obj)


#loading parameters...
with open('settings.json') as file:
    settings = dict_to_object(json.load(file))
