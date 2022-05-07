from typing import Tuple

from transformers import Conversation

from .base import BasePipeline


class Conversational(BasePipeline):
    def __init__(self, model: str = None, device: int = -1):
        if model is None:
            model = "microsoft/DialoGPT-large"
        super().__init__(name="conversational", options={"model": model}, device=device)
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
