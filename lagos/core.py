# -*- coding: utf-8 -*-
from typing import Union

import requests
import pandoc
from pandoc import types

from lagos.utils import sanitize

WIKI_URL = "https://en.wikipedia.org/wiki"


def get_article(title: str):
    raw_article = get_page(f"{WIKI_URL}/{sanitize(title)}")
    if raw_article is None:
        return "ERROR: Could not fetch"
    article_document = pandoc.read(source=raw_article, format="mediawiki")
    return article_document


def get_page(url: str) -> Union[str, None]:
    params = {"action": "raw"}
    r = requests.get(url, params=params)
    if r.status_code >= 300:
        return None
    return r.text
