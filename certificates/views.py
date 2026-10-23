"""Страницы сертификатов. Данные читаются из SQLite."""

import sqlite3

from django.shortcuts import render

from db.database import get_connection

CERTIFICATE_SQL = """
SELECT
    certificates.id,
    certificates.number,
    certificates.issued_at,
    certificates.is_revoked,
    events.title AS event_title,
    users.full_name AS user_name,
    results.score AS score
FROM certificates
JOIN events ON certificates.event_id = events.id
JOIN users ON certificates.user_id = users.id
JOIN results ON certificates.result_id = results.id
"""


def certificates(request):
    """Список сертификатов со связанными данными."""
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            CERTIFICATE_SQL + " ORDER BY certificates.id"
        ).fetchall()
        active_count = connection.execute(
            """
            SELECT COUNT(*) AS active_certificates
            FROM certificates
            WHERE is_revoked = 0
            """
        ).fetchone()
    finally:
        connection.close()
    return render(
        request,
        "certificates/certificate_list.html",
        {
            "certificates": rows,
            "active_count": active_count["active_certificates"],
        },
    )


def certificate_detail(request, certificate_id):
    """Карточка сертификата. Нет записи — ответ 404."""
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    try:
        certificate = connection.execute(
            CERTIFICATE_SQL + " WHERE certificates.id = ?",
            [certificate_id],
        ).fetchone()
    finally:
        connection.close()
    return render(
        request,
        "certificates/certificate_detail.html",
        {"certificate": certificate},
        status=404 if certificate is None else 200,
    )


def statistics(request):
    """Число сертификатов по мероприятиям и отбор групп через HAVING."""
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    try:
        by_event = connection.execute(
            """
            SELECT
                events.title AS event_title,
                COUNT(certificates.id) AS certificates_count
            FROM events
            LEFT JOIN certificates
                ON events.id = certificates.event_id
                AND certificates.is_revoked = 0
            GROUP BY events.id, events.title
            ORDER BY certificates_count DESC
            """
        ).fetchall()
        popular = connection.execute(
            """
            SELECT
                events.title AS event_title,
                COUNT(certificates.id) AS certificates_count
            FROM events
            JOIN certificates
                ON events.id = certificates.event_id
            GROUP BY events.id, events.title
            HAVING COUNT(certificates.id) > 1
            ORDER BY certificates_count DESC
            """
        ).fetchall()
    finally:
        connection.close()
    return render(
        request,
        "certificates/statistics.html",
        {"statistics": by_event, "popular": popular},
    )
