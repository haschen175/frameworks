"""Страницы мероприятий. Данные читаются из SQLite."""

import sqlite3

from django.shortcuts import render

from db.database import get_connection


def events(request):
    """Список мероприятий из таблицы events."""
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """
            SELECT id, title, event_date, description, min_score
            FROM events
            ORDER BY title
            """
        ).fetchall()
    finally:
        connection.close()
    return render(request, "events/event_list.html", {"events": rows})


def event_detail(request, event_id):
    """Карточка мероприятия. Нет записи — ответ 404."""
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    try:
        event = connection.execute(
            """
            SELECT id, title, event_date, description, min_score
            FROM events
            WHERE id = ?
            """,
            [event_id],
        ).fetchone()
    finally:
        connection.close()
    return render(
        request,
        "events/event_detail.html",
        {"event": event},
        status=404 if event is None else 200,
    )


def events_available(request):
    """Мероприятия без действующего сертификата в выбранный день."""
    event_date = request.GET.get("event_date", "").strip()
    rows = []
    if event_date:
        connection = get_connection()
        connection.row_factory = sqlite3.Row
        try:
            rows = connection.execute(
                """
                SELECT id, title, event_date, min_score
                FROM events
                WHERE id NOT IN (
                    SELECT event_id
                    FROM certificates
                    WHERE substr(issued_at, 1, 10) = ?
                        AND is_revoked = 0
                )
                ORDER BY title
                """,
                [event_date],
            ).fetchall()
        finally:
            connection.close()
    return render(
        request,
        "events/event_available.html",
        {"events": rows, "event_date": event_date},
    )
