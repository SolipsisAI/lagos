# -*- coding: utf-8 -*-
from datetime import datetime


def sanitize_wiki_title(title) -> str:
    return title.strip().rstrip("|").lower().replace(" ", "_")


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


class CustomDict(dict):
    """From https://stackoverflow.com/a/19399198"""

    def __init__(self, factory, key_name):
        self.factory = factory
        self.key_name = key_name

    def __missing__(self, key):
        kwargs = {self.key_name: key}
        self[key] = self.factory(**kwargs)
        return self[key]
