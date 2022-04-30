# -*- coding: utf-8 -*-
from typing import Union

import requests
import pandoc
from pandoc import types

from lagos.utils import sanitize

WIKI_URL = "https://en.wikipedia.org/wiki"
API_URL = "https://en.wikipedia.org/w/api.php"


def get_article(title: str, response_only: bool = False):
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
        "exsectionformat": "plain",
    }

    data = get_page(f"{API_URL}", params=params, response_only=response_only)
    results = data["query"]["pages"]
    pages = [page["extract"] for pageid, page in results.items()]

    text = "".join(pages)

    return "\n".join(text.split("\n"))


def get_page(
    url: str, format: str = "json", params=None, response_only: bool = False
) -> Union[str, None]:
    if params is None:
        params = {"action": "raw"}

    r = requests.get(url, params=params)

    if response_only:
        return r

    if r.status_code >= 300:
        return None

    if format != "json":
        return r.text

    return r.json()
