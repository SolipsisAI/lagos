from typing import List

import wikipediaapi

from lagos.data_source.base import BaseDataSource
from lagos.utils import sanitize

NAME = "wikipedia"


class WikipediaDataSource(BaseDataSource):
    def __init__(self, flatten: bool = True):
        super().__init__(NAME)
        self.wiki = wikipediaapi.Wikipedia(
            "en",
            extract_format=wikipediaapi.ExtractFormat.WIKI,
        )
        self.flatten = flatten

    def get_text(self, keyword, exclude: List[str] = None) -> str:
        page = self.wiki.page(sanitize(keyword))
        text = self.process_sections(page.sections, exclude=exclude)

        if self.flatten:
            text = text.replace("\n", " ")

        return text

    def process_sections(self, sections, text: str = "", exclude: List[str] = None):
        for section in sections:
            if exclude and section.title in exclude:
                continue
            text += self.process_sections(section.sections, section.text, exclude)

        return text
