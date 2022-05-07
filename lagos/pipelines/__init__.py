from .question_answering import QuestionAnswering
from .summarization import Summarization
from .conversational import Conversational

PIPELINES = {
    "question-answering": QuestionAnswering,
    "summarization": Summarization,
    "conversational": Conversational,
}


def load_pipeline(name, model):
    if name not in PIPELINES:
        raise ValueError(f"Pipeline {name} not found")
    return PIPELINES[name](model=model)
