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
        daemon: bool = False
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

        return msg

    def run(self):
        self.load_pipeline()
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
            {"author_id": self.bot_id, "conversation_id": conversation_id, "text": text}
        )

        store.insert_message(self.con, response)

        self.q.task_done()

        return self.last_event


bot = Bot(daemon=True)


if __name__ == "__main__":
    while True:
        text = input("> ")

        if not text:
            continue
        if text in ["/quit", "/q"]:
            break

        bot.add(MessageRecord({"author_id": 2, "text": text, "conversation_id": 1}))
