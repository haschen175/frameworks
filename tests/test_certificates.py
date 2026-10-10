"""Тесты пользователей и выдачи сертификатов."""

from datetime import date

from models.certificates import (
    get_certificate_status,
    issue_certificate,
    revoke_certificate,
)
from models.events import add_event
from models.results import add_result
from models.users import add_user, find_user


def test_add_and_find_user():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    assert len(users) == 1
    assert find_user(users, "петров")
    assert add_user(users, "Другой", "ivan@example.com") is None


def test_issue_certificate_for_passed_result():
    users = []
    events = []
    results = []
    certificates = []
    user = add_user(users, "Иван Петров", "ivan@example.com")
    event = add_event(events, "Python", date(2026, 10, 15), "", 60)
    result = add_result(results, user, event, 85)
    certificate = issue_certificate(certificates, result)
    assert certificate is not None
    assert certificate.is_active
    assert get_certificate_status(certificate.is_active) == (
        "Сертификат действует"
    )


def test_certificate_refused_when_score_is_low():
    users = []
    events = []
    results = []
    certificates = []
    user = add_user(users, "Мария Петрова", "maria@example.com")
    event = add_event(events, "Python", date(2026, 10, 15), "", 60)
    result = add_result(results, user, event, 45)
    assert issue_certificate(certificates, result) is None
    assert certificates == []


def test_duplicate_certificate_forbidden():
    users = []
    events = []
    results = []
    certificates = []
    user = add_user(users, "Иван Петров", "ivan@example.com")
    event = add_event(events, "Python", date(2026, 10, 15), "", 60)
    result = add_result(results, user, event, 90)
    first = issue_certificate(certificates, result)
    second = issue_certificate(certificates, result)
    assert first is second
    assert len(certificates) == 1


def test_revoke_certificate():
    users = []
    events = []
    results = []
    certificates = []
    user = add_user(users, "Иван Петров", "ivan@example.com")
    event = add_event(events, "Python", date(2026, 10, 15), "", 60)
    result = add_result(results, user, event, 90)
    certificate = issue_certificate(certificates, result)
    assert revoke_certificate(certificates, certificate.id)
    assert not certificate.is_active
    assert get_certificate_status(False) == "Сертификат аннулирован"
