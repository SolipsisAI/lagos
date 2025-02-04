import sqlite3

from pathlib import Path
from datetime import datetime

from lagos.records import UserRecord, MessageRecord


DB_NAME = "lagos.db"


def load(
    name: str = DB_NAME,
) -> sqlite3.Connection:
    db_exists = Path(name).exists()
    con = sqlite3.connect(name, check_same_thread=False)

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
            conversation_id TEXT,
            text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """
    )

    # Save (commit) the changes
    con.commit()

    # Setup
    setup_users(con)

    return con


def setup_users(con: sqlite3.Connection):
    # Bot
    insert_user(con, UserRecord({"name": "Erica", "is_bot": True}))
    # User
    insert_user(con, UserRecord({"name": "bitjockey", "is_bot": False}))


def insert_message(
    con: sqlite3.Connection, message: MessageRecord
) -> sqlite3.Connection:
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO messages VALUES(?, ?, ?, ?, ?)
        """,
        (
            None,
            message.author_id,
            message.conversation_id,
            message.text,
            message.timestamp,
        ),
    )

    con.commit()

    return last_message(con)


def insert_user(con: sqlite3.Connection, user: UserRecord) -> UserRecord:
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO users VALUES(?, ?, ?)
        """,
        (None, user.name, user.is_bot),
    )

    con.commit()

    return last_user(con)


def last_user(con: sqlite3.Connection):
    cur = con.cursor()

    cur.execute("SELECT * FROM users ORDER BY id DESC")

    result = cur.fetchone()
    return UserRecord(result)


def get_messages(con: sqlite3.Connection):
    cur = con.cursor()

    cur.execute(
        """
        SELECT
            m.*,
            u.name as username
        FROM messages m
        INNER JOIN users u ON m.author_id = u.id
        ORDER BY messages.timestamp ASC
        """
    )
    results = cur.fetchall()

    return list(map(MessageRecord, results))


def last_message(con: sqlite3.Connection):
    cur = con.cursor()

    cur.execute(
        """
        SELECT
            m.*,
            u.name as username
        FROM messages m
        INNER JOIN users u ON m.author_id = u.id
        ORDER BY timestamp DESC
        """
    )
    result = cur.fetchone()

    return MessageRecord(result) if result else None


def get_user(con: sqlite3.Connection, name: str):
    cur = con.cursor()

    cur.execute("SELECT * FROM users WHERE name = ?", [name])
    result = cur.fetchone()

    return UserRecord(result) if result else None


def get_users(con: sqlite3.Connection):
    cur = con.cursor()

    cur.execute("SELECT * FROM users")
    results = cur.fetchall()

    return list(map(UserRecord, results))
