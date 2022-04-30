# -*- coding: utf-8 -*-
import wikipediaapi

from lagos.utils import sanitize


def section_text(
    section: wikipediaapi.WikipediaPageSection,
    level: int = 0,
):
    if not section.sections:
        return section.text

    level += 1

    return section.text + section_text(section.sections[level], level)


def get_page(title) -> str:
    wiki = wikipediaapi.Wikipedia(
        "en",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
    )
    page = wiki.page(sanitize(title))

    return page
