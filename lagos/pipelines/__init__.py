from argparse import ArgumentError
from .question_answering import QuestionAnswering
from .summarization import Summarization
from .conversational import Conversational

PIPELINES = {
    "question-answering": QuestionAnswering,
    "summarization": Summarization,
    "conversational": Conversational,
}


def load_pipeline(name):
    if name not in PIPELINES:
        raise ArgumentError(f"Pipeline {name} not found")
    return PIPELINES[name]()
