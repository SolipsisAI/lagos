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
        await self.add(message)
        await self.respond()

    async def add(self, message: MessageRecord):
        """Receive an input message"""
        msg = store.insert_message(self.con, message)
        self.q.put(msg, block=False)

        return msg

    async def respond(self):
        """Response to the last message"""
        self.load_pipeline()

        received = self.q.get(block=False)

        conversation_id = received.conversation_id
        conversation_id, conversation = self.pipeline.predict(
            conversation_id=conversation_id, text=received.text
        )
        text = conversation.generated_responses[-1]
        response = MessageRecord(
            {"author_id": 1, "conversation_id": conversation_id, "text": text}
        )

        store.insert_message(self.con, response)

        self.q.task_done()

        print(response)

        return self.last_event
