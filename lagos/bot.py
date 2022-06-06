from lagos.pipelines import load_pipeline

from lagos import store
from lagos.records import UserRecord, MessageRecord
from lagos.utils import timestamp


class BotEvent:
    def __init__(self, username: str, text: str, conversation_id=None):
        self.timestamp = timestamp()
        self.username = username
        self.text = text
        self.conversation_id = conversation_id


class Bot:
    def __init__(self, model: str = "microsoft/DialoGPT-medium"):
        self.model = model
        self.con = store.load()
        self.pipeline = None

    @property
    def last_event(self):
        return store.last_message(self.con)

    def load_pipeline(self):
        if self.pipeline is None:
            self.pipeline = load_pipeline("conversational", model=self.model)

    def receive(self, message: MessageRecord):
        """Receive an input message"""
        store.insert_message(self.con, message)

        return self.last_event

    async def respond(self):
        """Response to the last message"""
        self.load_pipeline()

        event = self.last_event

        conversation_id = event.conversation_id
        conversation_id, conversation = self.pipeline.predict(
            conversation_id=conversation_id, text=event.text
        )
        text = conversation.generated_responses[-1]
        response_event = BotEvent(
            username="bot", text=text, conversation_id=conversation_id
        )
        self.history.append(response_event)
        self.responses.append(response_event)

        return self.last_event
