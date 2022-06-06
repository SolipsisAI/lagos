import tempfile

from persistqueue import Queue

from lagos.pipelines import load_pipeline

from lagos import store
from lagos.records import MessageRecord


class Bot:
    def __init__(self, model: str = "microsoft/DialoGPT-medium"):
        self.model = model
        self.con = store.load()
        self.pipeline = None
        dirpath = tempfile.mkdtemp()
        self.q = Queue(dirpath)

    @property
    def last_event(self):
        return store.last_message(self.con)

    def load_pipeline(self):
        if self.pipeline is None:
            self.pipeline = load_pipeline("conversational", model=self.model)

    async def receive(self, message: MessageRecord):
        """Receive an input message"""
        store.insert_message(self.con, message)

        self.q.put(self.last_event, block=False)

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
        message = MessageRecord(
            {"author_id": 1, "conversation_id": conversation_id, "text": text}
        )

        store.insert_message(self.con, message)

        return self.last_event
