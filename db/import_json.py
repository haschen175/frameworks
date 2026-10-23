"""Перенос данных проекта из JSON-файлов в SQLite."""

import json
from pathlib import Path

from db.database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / "data" / "users.json"
EVENTS_FILE = BASE_DIR / "data" / "events.json"
RESULTS_FILE = BASE_DIR / "data" / "results.json"
CERTIFICATES_FILE = BASE_DIR / "data" / "certificates.json"


def load_json(filename):
    """Прочитать JSON-файл проекта."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def clear_tables(connection):
    """Очистить таблицы перед повторным переносом."""
    connection.execute("DELETE FROM certificates")
    connection.execute("DELETE FROM results")
    connection.execute("DELETE FROM events")
    connection.execute("DELETE FROM users")


def import_users(connection):
    """Перенести пользователей."""
    users = load_json(USERS_FILE)
    connection.executemany(
        """
        INSERT INTO users (id, full_name, email, role)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                user["id"],
                user["full_name"],
                user["email"],
                user["role"],
            )
            for user in users
        ],
    )


def import_events(connection):
    """Перенести мероприятия."""
    events = load_json(EVENTS_FILE)
    connection.executemany(
        """
        INSERT INTO events (
            id, title, event_date, description, min_score
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                event["id"],
                event["title"],
                event["date"],
                event.get("description", ""),
                event["min_score"],
            )
            for event in events
        ],
    )


def import_results(connection):
    """Перенести результаты участия."""
    results = load_json(RESULTS_FILE)
    connection.executemany(
        """
        INSERT INTO results (
            id, user_id, event_id, score, passed
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                result["id"],
                result["user_id"],
                result["event_id"],
                result["score"],
                int(result["passed"]),
            )
            for result in results
        ],
    )


def import_certificates(connection):
    """Перенести сертификаты."""
    certificates = load_json(CERTIFICATES_FILE)
    connection.executemany(
        """
        INSERT INTO certificates (
            id,
            user_id,
            event_id,
            result_id,
            number,
            issued_at,
            is_revoked
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                certificate["id"],
                certificate["user_id"],
                certificate["event_id"],
                certificate["result_id"],
                certificate["number"],
                certificate["issued_at"],
                int(certificate["is_revoked"]),
            )
            for certificate in certificates
        ],
    )


def main():
    """Выполнить перенос и сохранить транзакцию."""
    connection = get_connection()
    try:
        clear_tables(connection)
        import_users(connection)
        import_events(connection)
        import_results(connection)
        import_certificates(connection)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
