from lagos.pipelines import load_pipeline

from lagos.utils import timestamp


class Event:
    def __init__(self, username: str, text: str, conversation_id=None):
        self.timestamp = timestamp()
        self.username = username
        self.text = text
        self.conversation_id = conversation_id


class Bot:
    def __init__(self, model: str = "microsoft/DialoGPT-medium"):
        self.model = model
        self.history = []
        self.pipeline = None

    @property
    def last_event(self):
        return self.history[-1] if self.history else None

    def load_pipeline(self):
        if self.pipeline is None:
            self.pipeline = load_pipeline("conversational", model=self.model)

    def receive(self, event: Event):
        """Receive an input message"""
        self.history.append(event)

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
        response_event = Event(
            username="bot", text=text, conversation_id=conversation_id
        )
        self.history.append(response_event)

        return self.last_event
