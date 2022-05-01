from lib2to3.pytree import Base
from transformers import Conversation

from .base import BasePipeline

OPTIONS = {
    "model": "microsoft/DialoGPT-medium",
}


class Conversational(BasePipeline):
    def __init__(self, device: int = -1):
        super().__init__("conversational", OPTIONS, device)

    def predict(self, text: str = None):
        return self.pipeline(Conversation(text))