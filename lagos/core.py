# -*- coding: utf-8 -*-
from typing import Union

import requests

from lagos.utils import sanitize

WIKI_URL = "https://en.wikipedia.org/wiki"


def get_article(title: str):
    raw_article = get_page(f"{WIKI_URL}/{sanitize(title)}")
    if raw_article is None:
        return "ERROR: Could not fetch"
    return raw_article


def get_page(url: str) -> Union[str, None]:
    params = {"action": "raw"}
    r = requests.get(url, params=params)
    if r.status_code >= 300:
        return None
    return r.text
