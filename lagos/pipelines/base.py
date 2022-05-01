from typing import Dict, List, Union
from collections import defaultdict
from xml.dom import ValidationErr

from transformers import pipeline

from lagos.data_source.wikipedia import WikipediaDataSource


class BasePipeline:
    def __init__(self, name: str, options: Dict = None, device: int = -1):
        self.options = options
        self.options["task"] = name
        self.options["device"] = device
        self.pipeline = pipeline(**options)
        self.data_sources = {"wiki": WikipediaDataSource()}
        self.context = defaultdict(list)

    def add_raw_context(self, keyword, context: Union[str, List]):
        if isinstance(context, list):
            context = " ".join(context)
        self.context[keyword].append(context)

    def add_context(self, keyword, exclude=None, data_source="wiki"):
        text = self.data_sources[data_source].get_text(keyword, exclude)
        self.context[keyword].append(text)

    def get_context(self, keyword):
        if keyword not in self.context:
            raise ValidationErr(f"{keyword} not found")
        return " ".join(self.context[keyword])

    def remove_context(self, keyword):
        if keyword not in self.context:
            raise ValidationErr(f"{keyword} not found")
        return self.context.pop(keyword)
