# -*- coding: utf-8 -*-
import wikipediaapi

from lagos.utils import sanitize


def get_article(title) -> str:
    wiki = wikipediaapi.Wikipedia(
        "en",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
    )
    page = wiki.page(sanitize(title))

    return page
