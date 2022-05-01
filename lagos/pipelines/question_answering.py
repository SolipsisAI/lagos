from lagos.pipelines.base import BasePipeline

OPTIONS = {
    "model": "bert-large-cased-whole-word-masking-finetuned-squad",
}
DATA_SOURCES = ["wiki"]


class QuestionAnswering(BasePipeline):
    def __init__(self, device: int = -1):
        super().__init__(
            name="question-answering",
            data_sources=DATA_SOURCES,
            options=OPTIONS,
            device=device,
        )

    def predict(self, question, keyword):
        context = self.get_context(keyword)
        return self.pipeline(question, context)
