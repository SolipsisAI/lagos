from argparse import ArgumentError
from typing import Dict, List, Union
from collections import defaultdict

from transformers import pipeline, Conversation

from lagos.data_source import load_data_source


class BasePipeline:
    def __init__(
        self, name: str, data_sources: List[str] = None, options: Dict = None, device: int = -1
    ):
        self.options = options
        self.options["task"] = name
        self.options["device"] = device
        self.pipeline = pipeline(**options)
        self.data_sources = {}
        self.context = defaultdict(list)
        self.load_data_sources(data_sources)

    def load_data_sources(self, data_sources: List[str]):
        if not data_sources:
            return

        for data_source in data_sources:
            self.data_sources[data_source] = load_data_source(data_source)

    def add_raw_context(self, keyword, context: Union[str, List, Conversation]):
        if isinstance(context, list):
            context = " ".join(context)
        self.context[keyword].append(context)

    def add_context(self, keyword, exclude=None, data_source="wiki"):
        text = self.data_sources[data_source].find(keyword, exclude=exclude)
        self.context[keyword].append(text)

    def get_context(self, keyword, flatten: bool = True):
        if keyword not in self.context:
            raise ArgumentError(f"{keyword} not found")
        if flatten:
            return " ".join(self.context[keyword])
        return self.context[keyword]

    def remove_context(self, keyword):
        if keyword not in self.context:
            raise ArgumentError(f"{keyword} not found")
        return self.context.pop(keyword)
