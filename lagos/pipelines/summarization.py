from .base import BasePipeline

OPTIONS = {
    "model": "t5-base",
    "tokenizer": "t5-base",
    "framework": "tf",
}


class Summarization(BasePipeline):
    def __init__(self, device: int = -1):
        super().__init__("summarization", OPTIONS, device)

    def predict(self, keyword, min_length=20, max_length=100):
        context = self.get_context(keyword)
        return self.pipeline(context, min_length=min_length, max_length=max_length)
