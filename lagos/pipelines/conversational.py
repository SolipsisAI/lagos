from typing import Tuple, Union

from transformers import Conversation

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
        self.context = {}

    def add_context(self, conversation_obj: Union[str, Conversation], text: str = None):
        conversation_id = None

        if isinstance(conversation_obj, Conversation):
            conversation_id = str(conversation_obj.uuid)
            self.context[conversation_id] = conversation_obj
        elif isinstance(conversation_obj, str):
            conversation_id = conversation_obj
            if conversation_id not in self.context:
                conversation = Conversation()
                conversation_id = str(conversation.uuid)
                self.context[conversation_id] = conversation
        
        if text:
            self.context[conversation_id].add_user_input(text)

        return conversation_id

    def get_context(self, conversation_id: str):
        return self.context.get(conversation_id)

    def predict(
        self, conversation_id: str = None, text: str = None
    ) -> Tuple[str, Conversation]:
        conversation_id = self.add_context(conversation_id, text)
        context = self.get_context(conversation_id)
        return conversation_id, self.pipeline(context)
