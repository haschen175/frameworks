"""Проверка веб-страниц Django."""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "certify.settings")
django.setup()

from django.test import Client  # noqa: E402


def test_home_page():
    response = Client().get("/")
    assert response.status_code == 200
    text = response.content.decode()
    assert "Сервис сертификатов" in text
    assert "Мероприятия" in text


def test_event_list_shows_data():
    response = Client().get("/events/")
    assert response.status_code == 200
    text = response.content.decode()
    assert "Python для начинающих" in text
    assert "Всего мероприятий" in text


def test_event_detail_and_missing():
    found = Client().get("/events/1/")
    assert found.status_code == 200
    assert "Вводный курс" in found.content.decode()
    missing = Client().get("/events/9999/")
    assert missing.status_code == 404
    assert "Мероприятие не найдено" in missing.content.decode()


def test_available_events_and_statistics():
    available = Client().get("/events/available/?event_date=2026-10-15")
    assert available.status_code == 200
    text = available.content.decode()
    assert "Олимпиада по информатике" in text
    assert "Python для начинающих" not in text
    statistics = Client().get("/certificates/statistics/")
    assert statistics.status_code == 200
    page = statistics.content.decode()
    assert "Действующих сертификатов" in page
    assert "Олимпиада по информатике" in page


def test_certificate_list_and_detail():
    listing = Client().get("/certificates/")
    assert listing.status_code == 200
    text = listing.content.decode()
    assert "CERT-20261015-0001" in text
    assert "Действует" in text
    assert "Аннулирован" in text
    detail = Client().get("/certificates/1/")
    assert detail.status_code == 200
    assert "Иванов Иван Иванович" in detail.content.decode()
    missing = Client().get("/certificates/9999/")
    assert missing.status_code == 404
