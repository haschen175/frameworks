"""Страницы мероприятий."""

from django.shortcuts import render

from models.events import find_event_by_id
from storage import load_events


def events(request):
    """Список мероприятий из JSON-хранилища."""
    context = {
        "events": load_events("data/events.json"),
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, event_id):
    """Карточка одного мероприятия. Нет объекта — ответ 404."""
    events_list = load_events("data/events.json")
    event = find_event_by_id(events_list, event_id)
    context = {
        "event": event,
    }
    return render(
        request,
        "events/event_detail.html",
        context,
        status=404 if event is None else 200,
    )
