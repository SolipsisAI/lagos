from xml.dom import ValidationErr
from transformers import Conversation

from .base import BasePipeline

OPTIONS = {
    "model": "microsoft/DialoGPT-medium",
}


class Conversational(BasePipeline):
    def __init__(self, device: int = -1):
        super().__init__("conversational", OPTIONS, device)
        self.context = {}
    
    def add_context(self, conversation_id: str, text: str):
        if conversation_id not in self.context:
            self.context[conversation_id] = Conversation()
        self.context[conversation_id].add_user_input(text)

    def get_context(self, conversation_id: str):
        return self.context.get(conversation_id)

    def predict(self, conversation_id: str = None, text: str = None):
        self.add_context(conversation_id, text)
        context = self.get_context(conversation_id)

        return self.pipeline(context)
