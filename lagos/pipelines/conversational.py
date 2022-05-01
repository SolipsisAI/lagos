from transformers import Conversation

from .base import BasePipeline

OPTIONS = {
    "model": "microsoft/DialoGPT-medium",
}


class Conversational(BasePipeline):
    def __init__(self, device: int = -1):
        super().__init__("conversational", OPTIONS, device)
        self.context = {}
    
    def add_context(self, conversation_id, text: str):
        if conversation_id not in self.context:
            conversation = Conversation() 
            conversation_id = conversation.uuid
            self.context[conversation_id] = conversation
        self.context[conversation_id].add_user_input(text)
        return conversation_id

    def get_context(self, conversation_id):
        return self.context[conversation_id]
    
    def predict(self, conversation_id=None, text=None):
        conversation_id = self.add_context(conversation_id, text)
        return self.get_context(conversation_id)