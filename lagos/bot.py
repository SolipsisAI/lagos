from pyclbr import Function
import threading
import tempfile

from persistqueue import Queue

from lagos.pipelines import load_pipeline

from lagos import store
from lagos.records import MessageRecord


class Bot:
    def __init__(
        self,
        *,
        name: str = "Erica",
        model: str = "microsoft/DialoGPT-medium",
        daemon: bool = False,
        callback: Function = None,
    ):
        self.thread = None
        self.pipeline = None

        # Model name
        self.model = model

        # Setup DB connection
        self.con = store.load()

        # Setup queue
        dirpath = tempfile.mkdtemp()
        self.q = Queue(dirpath)

        # Get users
        # bot_user = store.get_user(self.con, name=name)
        # self.bot_id = bot_user.id
        self.bot_id = 1

        # Threading
        if daemon:
            self.callback = callback
            self.thread = threading.Thread(target=self.run, args=())
            self.daemon = True
            self.thread.start()

    @property
    def last_event(self):
        return store.last_message(self.con)

    def load_pipeline(self):
        if self.pipeline is None:
            self.pipeline = load_pipeline("conversational", model=self.model)

    def add(self, message: MessageRecord):
        """Receive an input message"""
        msg = store.insert_message(self.con, message)
        self.q.put(msg)

        if self.callback:
            self.callback(msg)

        return msg

    def run(self):
        self.load_pipeline()
        while True:
            if self.q.empty():
                continue
            self.respond()

            if self.callback:
                self.callback(self.last_event)

    def respond(self):
        """Response to the last message"""
        received = self.q.get()

        conversation_id = received.conversation_id
        conversation_id, conversation = self.pipeline.predict(
            conversation_id=conversation_id, text=received.text
        )

        text = conversation.generated_responses[-1]

        response = MessageRecord(
            {"author_id": self.bot_id, "conversation_id": conversation_id, "text": text}
        )

        store.insert_message(self.con, response)

        self.q.task_done()

        return self.last_event


if __name__ == "__main__":
    bot = Bot(daemon=True)
    while True:
        text = input("> ")

        if not text:
            continue
        if text in ["/quit", "/q"]:
            break

        bot.add(MessageRecord({"author_id": 2, "text": text, "conversation_id": 1}))
