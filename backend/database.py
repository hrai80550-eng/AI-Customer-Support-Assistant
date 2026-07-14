import os
import sqlite3
from pathlib import Path


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent.parent / "database" / "customer_support_chatbot.db"


def get_database_path():
    database_path = Path(os.environ.get("DATABASE_PATH", DEFAULT_DATABASE_PATH))
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return database_path


def initialize_database(connection):
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            message_text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
        );

        CREATE TABLE IF NOT EXISTS intents (
            intent_id INTEGER PRIMARY KEY AUTOINCREMENT,
            intent_name TEXT NOT NULL UNIQUE,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS responses (
            response_id INTEGER PRIMARY KEY AUTOINCREMENT,
            intent_id INTEGER NOT NULL,
            response_text TEXT NOT NULL,
            FOREIGN KEY (intent_id) REFERENCES intents (intent_id)
        );

        INSERT OR IGNORE INTO conversations (conversation_id, user_id)
        VALUES (1, 'web-user');
        """
    )
    connection.commit()


def get_db_connection():
    connection = sqlite3.connect(get_database_path())
    connection.execute("PRAGMA foreign_keys = ON")
    initialize_database(connection)
    return connection
