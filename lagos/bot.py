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
        self.pipeline = load_pipeline("conversational", model=self.model)
        self.history = []

    def respond(self, event: Event):
        self.history.append(event)

        conversation_id = event.conversation_id
        conversation_id, conversation = self.pipeline.predict(
            conversation_id=conversation_id, text=event.text
        )
        text = conversation.generated_responses[-1]
        response_event = Event(
            username="bot", text=text, conversation_id=conversation_id
        )
        self.history.append(response_event)

        return self.history[-1]
