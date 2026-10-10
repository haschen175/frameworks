"""Тесты мероприятий."""

from datetime import date

from models.events import (
    add_event,
    check_event_score,
    filter_events_by_min_score,
    find_event,
    sort_events,
)


def test_add_event():
    events = []
    add_event(events, "Аудиторный курс", date(2026, 10, 15), "", 60)
    assert len(events) == 1
    assert events[0].title == "Аудиторный курс"


def test_find_event():
    events = []
    add_event(events, "Python для начинающих", date(2026, 10, 15))
    assert find_event(events, "python")


def test_check_event_score():
    events = []
    add_event(events, "Олимпиада", date(2026, 11, 20), "", 75)
    assert check_event_score(events, 1, 80)
    assert not check_event_score(events, 1, 70)


def test_filter_and_sort_events():
    events = []
    add_event(events, "Бета", date(2026, 12, 1), "", 80)
    add_event(events, "Альфа", date(2026, 1, 1), "", 40)
    selected = filter_events_by_min_score(events, 70)
    assert len(selected) == 1
    ordered = sort_events(events, by="title")
    assert ordered[0].title == "Альфа"
