# -*- coding: utf-8 -*-
import wikipediaapi

from lagos.utils import sanitize


def process_sections(sections, level: int = 0, text: str = ""):
    for section in sections:
        print(section.title)
        text += process_sections(section.sections, level + 1, section.text)
    return text


def get_page(title) -> str:
    wiki = wikipediaapi.Wikipedia(
        "en",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
    )
    page = wiki.page(sanitize(title))

    return page
