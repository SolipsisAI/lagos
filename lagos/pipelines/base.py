from typing import Dict

from transformers import pipeline


class BasePipeline:
    def __init__(self, name: str, options: Dict = None):
        self.options = options
        self.options["task"] = name
        self.pipeline = pipeline(**options)
