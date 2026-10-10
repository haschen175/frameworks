"""Страницы сертификатов."""

from django.shortcuts import render

from models.certificates import find_certificate_by_id
from storage import (
    load_certificates,
    load_events,
    load_results,
    load_users,
)


def _load_certificates():
    """Загрузить сертификаты вместе со связанными объектами."""
    users = load_users("data/users.json")
    events = load_events("data/events.json")
    results = load_results("data/results.json", users, events)
    return load_certificates(
        "data/certificates.json",
        users,
        events,
        results,
    )


def certificates(request):
    """Список сертификатов."""
    context = {
        "certificates": _load_certificates(),
    }
    return render(
        request,
        "certificates/certificate_list.html",
        context,
    )


def certificate_detail(request, certificate_id):
    """Карточка сертификата. Нет объекта — ответ 404."""
    certificate = find_certificate_by_id(
        _load_certificates(),
        certificate_id,
    )
    context = {
        "certificate": certificate,
    }
    return render(
        request,
        "certificates/certificate_detail.html",
        context,
        status=404 if certificate is None else 200,
    )
