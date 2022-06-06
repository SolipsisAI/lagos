import sqlite3

from pathlib import Path
from datetime import datetime


DB_NAME = "lagos.db"


def load(name: str = DB_NAME) -> sqlite3.Connection:
    db_exists = Path(name).exists()
    con = sqlite3.connect(name)

    if not db_exists:
        con = create(con)

    return con


def create(con: sqlite3.Connection) -> sqlite3.Connection:
    cur = con.cursor()

    # Create table
    cur.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT,
            is_bot INTEGER DEFAULT 0
        );
        """
    )

    # Create messages
    cur.execute(
        """
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            author_id INTEGER NOT NULL,
            recipient_id INTEGER NOT NULL,
            text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """
    )

    # Save (commit) the changes
    con.commit()

    return con


def insert_message(
    con: sqlite3.Connection, author_id: int, recipient_id: int, text: str
) -> sqlite3.Connection:
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO messages VALUES(?, ?, ?, ?, ?)
        """,
        (None, author_id, recipient_id, text, datetime.now().isoformat()),
    )

    con.commit()

    return con


def insert_user(
    con: sqlite3.Connection, name: str, is_bot: bool = False
) -> sqlite3.Connection:
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO users VALUES(?, ?, ?)
        """,
        (None, name, is_bot),
    )

    con.commit()

    return con
