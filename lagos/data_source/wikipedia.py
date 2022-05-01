from typing import Any, List

import wikipediaapi

from lagos.data_source.base import BaseDataSource
from lagos.utils import sanitize_wiki_title

NAME = "wikipedia"


class WikipediaDataSource(BaseDataSource):
    def __init__(self):
        super().__init__(NAME)
        self.wiki = wikipediaapi.Wikipedia(
            "en",
            extract_format=wikipediaapi.ExtractFormat.WIKI,
        )

    def query_sections(self, key, update: bool = False):
        return list(self.query(key, update=update).keys())

    def find(self, key, exclude: List[str] = None) -> str:
        page = self.wiki.page(self.sanitize(key))
        results = self.process_page(
            page=page,
            exclude=exclude,
        )
        return results

    def process_page(self, page, exclude: List[str] = None):
        root_key = self.sanitize(page.title)
        results = {}

        def process_sections(sections, key: str, text: str = ""):
            for section in sections:
                if exclude and section.title in exclude:
                    continue

                section_key = self.sanitize(section.title)
                result_key = "|".join([key, section_key])

                results[result_key] = process_sections(
                    sections=section.sections,
                    key=result_key,
                    text=section.text,
                )

            return text

        process_sections(page.sections, key=root_key)

        return results

    def sanitize(self, key):
        return sanitize_wiki_title(key)
