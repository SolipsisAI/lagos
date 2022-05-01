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

    def find(self, key, exclude: List[str] = None) -> str:
        page = self.wiki.page(self.sanitize(key))
        results = self.process_page(
            page=page,
            exclude=exclude,
        )
        return results

    def process_page(self, page, exclude: List[str] = None):
        root_key = self.sanitize(page.title)
        results = []

        def process_sections(sections, key: str = "", text: str = ""):
            for section in sections:
                if exclude and section.title in exclude:
                    continue
                section_key = self.sanitize(section.title)
                result_key = "-".join([root_key, section_key])
                results.append(
                    (
                        result_key,
                        process_sections(section.sections, section.title, section.text),
                    )
                )
            return (key, text)

        process_sections(page.sections)

        return results

    def sanitize(self, key):
        return sanitize_wiki_title(key)
