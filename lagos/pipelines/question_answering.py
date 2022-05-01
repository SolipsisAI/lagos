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

    def add_context(self, keyword, exclude=None, data_source="wiki"):
        text = self.data_sources[data_source].get_page_text(keyword, exclude)
        self.context[keyword].append(text)

    def predict(self, question, keyword=None):
        context = self.context.get(keyword)
        if not context:
            raise ValidationErr(f"{keyword} not found in context")
        return self.pipeline(question, " ".join(context))
