import threading

from persistqueue import SQLiteQueue

from lagos.pipelines import load_pipeline

from lagos import store
from lagos.records import MessageRecord


class Bot:
    def __init__(
        self,
        *,
        name: str = "Erica",
        model: str = "microsoft/DialoGPT-large",
        daemon: bool = False,
        callback=None,
    ):
        self.name = name
        self.bot_user = None
        self.thread = None
        self.pipeline = None

        # Model name
        self.model = model

        # Setup DB connection
        self.con = store.load()

        # Setup queue
        self.q = SQLiteQueue(".lagos_queue", multithreading=daemon)

        # Run the bot in a different thread
        if daemon:
            self.callback = callback
            self.thread = threading.Thread(target=self.run, args=(), daemon=daemon)
            self.thread.start()

    @property
    def last_event(self):
        return store.last_message(self.con)

    def load_resources(self):
        # Get bot user
        if not bool(self.bot_user):
            self.bot_user = store.get_user(self.con, name=self.name)

        # Load pipeline
        if not bool(self.pipeline):
            self.pipeline = load_pipeline("conversational", model=self.model)

    async def add(self, message: MessageRecord):
        """Receive an input message"""
        msg = store.insert_message(self.con, message)
        self.q.put(msg)

        if bool(self.callback) and self.callback:
            self.callback(msg)

        return msg

    def run(self):
        self.load_resources()

        while True:
            if self.q.empty():
                continue
            self.respond()

    def respond(self):
        """Response to the last message"""
        received = self.q.get()

        conversation_id = received.conversation_id
        conversation_id, conversation = self.pipeline.predict(
            conversation_id=conversation_id, text=received.text
        )

        text = conversation.generated_responses[-1]

        response = MessageRecord(
            {
                "author_id": self.bot_user.id,
                "conversation_id": conversation_id,
                "text": text,
            }
        )

        store.insert_message(self.con, response)

        self.q.task_done()

        if bool(self.callback):
            self.callback(self.last_event)

        return self.last_event
