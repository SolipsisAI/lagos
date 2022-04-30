# -*- coding: utf-8 -*-
import wikipediaapi

from lagos.utils import sanitize


def process_sections(sections, text: str = "", exclude: str = None):
    for section in sections:
        if exclude and section.title.lower() in exclude.lower().split("|"):
            continue
        text += process_sections(section.sections, section.text, exclude)
    return text


def get_page_text(title, flatten: bool = False, exclude=None) -> str:
    wiki = wikipediaapi.Wikipedia(
        "en",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
    )
    page = wiki.page(sanitize(title))

    text = process_sections(page.sections, exclude=exclude)

    if flatten:
        text = text.replace("\n", " ")

    return text
