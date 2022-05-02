from typing import Any, Dict, List

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
        result = self.query(key, update=update)
        if isinstance(result, Dict):
            return list(result.keys())
        return [key]

    def find(self, key, exclude=None):
        page = self.wiki.page(self.sanitize(key))
        results = self.process_page(
            page=page,
            exclude=exclude,
        )
        return results

    def process_page(self, page, exclude=None):
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
