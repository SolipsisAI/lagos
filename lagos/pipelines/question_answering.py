from collections import defaultdict
from xml.dom import ValidationErr

from lagos.pipelines.base import BasePipeline
from lagos.data_source.wikipedia import WikipediaDataSource

OPTIONS = {
    "model": "bert-large-cased-whole-word-masking-finetuned-squad",
}


class QuestionAnswering(BasePipeline):
    def __init__(self):
        super().__init__("question-answering", OPTIONS)
        self.data_sources = {
            "wiki": WikipediaDataSource(),
        }
        self.context = defaultdict(list)

    def predict(self, question, keyword):
        context = self.get_context(keyword)
        return self.pipeline(question, context)
