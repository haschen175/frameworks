"""Подключение Python к базе SQLite проекта."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "certify.sqlite"


def get_connection():
    """Открыть соединение и включить проверку внешних ключей."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
