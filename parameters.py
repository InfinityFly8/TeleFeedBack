import logging
import json
from contextlib import suppress
from types import SimpleNamespace

import emoji

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


class Banlist:
    def __init__(self):
        with suppress(FileExistsError):
            open('banlist', 'x').close()
        self._banlist = set()
        with open('banlist') as file:
            for line in file:
                try:
                    self._banlist.add(int(line))
                except ValueError:
                    settings_logger.warn('Unresolved value %s' % line)
                    continue
    
    def add(self, value: int):
        # Type Check
        value = int(value)
        
        if value not in self._banlist:
            self._banlist.add(value)
            with open('banlist', 'a') as file:
                file.write(str(value) + '\n')
            return True
        return False
    
    def remove(self, value: int):
        # Type Check
        value = int(value)
        if value in self._banlist:
            self._banlist.remove(value)
            with open('banlist', 'w') as file:
                for id in self._banlist:
                    file.write(str(id) + '\n')
    
    def __contains__(self, value):
        return int(value) in self._banlist


with open('settings.json') as file:
    settings = dict_to_object(json.load(file))
banlist = Banlist()
