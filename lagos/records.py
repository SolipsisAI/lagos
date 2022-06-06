from datetime import datetime

from typing import Tuple, Union, Dict


class UserRecord:
    def __init__(self, row: Union[Tuple, Dict]) -> None:
        if isinstance(row, tuple):
            self.id = row[0]
            self.name = row[1]
            self.is_bot = bool(row[2])
        elif isinstance(row, dict):
            self.id = row.get("id")
            self.name = row.get("name")
            self.is_bot = row.get("is_bot")

    def __repr__(self) -> str:
        return f"""
        (User)
        id: {self.id}
        name: {self.name}
        is_bot: {self.is_bot}
        """


class MessageRecord:
    def __init__(self, row: Union[Tuple, Dict]) -> None:
        if isinstance(row, tuple):
            self.id = row[0]
            self.author_id = row[1]
            self.conversation_id = row[2]
            self.text = row[3]
            self.timestamp = row[4]
        elif isinstance(row, dict):
            self.id = row.get("id")
            self.author_id = row.get("author_id")
            self.conversation_id = row.get("conversation_id")
            self.text = row.get("text")
            self.timestamp = row.get("timestamp", datetime.now().isoformat())

    def __repr__(self) -> str:
        return f"""
        (Message)
        id: {self.id}
        author_id: {self.author_id}
        conversation_id: {self.conversation_id}
        text: {self.text}
        timestamp: {self.timestamp}
        """
