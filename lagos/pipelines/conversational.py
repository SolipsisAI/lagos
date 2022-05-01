from typing import Tuple

from transformers import Conversation

from .base import BasePipeline

OPTIONS = {
    "model": "microsoft/DialoGPT-large",
}


class Conversational(BasePipeline):
    def __init__(self, device: int = -1):
        super().__init__(name="conversational", options=OPTIONS, device=device)
        self.context = {}

    def add_context(self, conversation_id: str, text: str):
        if conversation_id not in self.context:
            conversation = Conversation()
            conversation_id = str(conversation.uuid)
            self.context[conversation_id] = conversation
        self.context[conversation_id].add_user_input(text)
        return conversation_id

    def get_context(self, conversation_id: str):
        return self.context[conversation_id]

    def predict(
        self, conversation_id: str = None, text: str = None
    ) -> Tuple[str, Conversation]:
        conversation_id = self.add_context(conversation_id, text)
        context = self.get_context(conversation_id)
        return conversation_id, self.pipeline(context)
