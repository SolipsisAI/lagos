import threading

import torch

from typing import Union

from persistqueue import SQLiteQueue
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
)

from lagos import store
from lagos.records import MessageRecord


class Bot:
    def __init__(
        self,
        *,
        name: str = "Erica",
        model: Union[str, PreTrainedModel] = "microsoft/DialoGPT-large",
        tokenizer: Union[str, PreTrainedTokenizer] = "microsoft/DialoGPT-large",
        daemon: bool = False,
        callback=None,
    ):
        self.name: str = name
        self.bot_user: MessageRecord = None
        self.thread: threading.Thread = None
        self.model: Union[str, PreTrainedModel] = model
        self.tokenizer: Union[str, PreTrainedTokenizer] = tokenizer

        self.chat_history_ids = []
        self.step = 0

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
        if not bool(self.bot_user):
            self.bot_user = store.get_user(self.con, name=self.name)

        if isinstance(self.model, str):
            self.model = AutoModelForCausalLM.from_pretrained(self.model)

        if isinstance(self.tokenizer, str):
            self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer)

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
        response_text = self.generate_responses(text=received.text)

        response = MessageRecord(
            {
                "author_id": self.bot_user.id,
                "text": response_text,
            }
        )

        store.insert_message(self.con, response)

        self.q.task_done()

        if bool(self.callback):
            self.callback(self.last_event)

        return self.last_event

    def generate_responses(self, text):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = self.tokenizer.encode(
            text + self.tokenizer.eos_token, return_tensors="pt"
        )

        # append the new user input tokens to the chat history
        bot_input_ids = (
            torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1)
            if self.step > 0
            else new_user_input_ids
        )

        # generated a response while limiting the total chat history to 1000 tokens,
        self.chat_history_ids = self.model.generate(
            bot_input_ids,
            max_length=512,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8,
        )

        response = self.tokenizer.decode(
            self.chat_history_ids[:, bot_input_ids.shape[-1] :][0],
            skip_special_tokens=True,
        )

        self.step += 1

        return response
