from uuid import uuid4

from transformers import Conversation

from lagos.utils import CustomDict
from .base import BasePipeline


class Conversational(BasePipeline):
    def __init__(self, model: str = None, tokenizer: str = None, device: int = -1):
        if model is None:
            model = "microsoft/DialoGPT-medium"

        if model is not None and tokenizer is None:
            # Use tokenizer from model
            tokenizer = model
        elif tokenizer is None:
            tokenizer = "microsoft/DialoGPT-medium"

        super().__init__(
            name="conversational",
            options={"model": model, "tokenizer": tokenizer},
            device=device,
        )
        self.context = CustomDict(Conversation, "conversation_id")

    def add_context(self, text: str, conversation_id: str = None):
        if conversation_id is None:
            conversation_id = str(uuid4())

        self.context[conversation_id].add_user_input(text)

        return conversation_id

    def get_context(self, conversation_id: str):
        print(self.context.get(conversation_id))
        return self.context.get(conversation_id)

    def predict(self, text: str = None, conversation_id: str = None) -> Conversation:
        conversation_id = self.add_context(text=text, conversation_id=conversation_id)
        context = self.get_context(conversation_id)
        return self.pipeline(context)
