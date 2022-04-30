# -*- coding: utf-8 -*-
from typing import Union, List, Dict

import tensorflow as tf

from lagos.utils import sanitize


WIKI_URL = "https://en.wikipedia.org/wiki"
API_URL = "https://en.wikipedia.org/w/api.php"


def get_articles(*titles):
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "exsectionformat": "plain",
    }

    params["titles"] = ("|".join(list(map(sanitize, titles))),)

    if len(titles) > 1:
        params["exintro"] = True

    data = get_page(f"{API_URL}", format="json", params=params)
    results = data["query"]["pages"]
    pages = [page.get("extract", "") for _, page in results.items()]
    text = "".join(pages)

    return "\n".join(text.split("\n"))


def get_page(url: str, format: str = "json", params=None) -> Union[str, Dict, None]:
    if params is None:
        params = {"action": "raw"}

    r = requests.get(url, params=params)

    if r.status_code >= 300:
        return None

    if format != "json":
        return r.text

    return r.json()
