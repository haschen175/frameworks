"""Тесты сохранения и загрузки JSON."""

from datetime import date

from models.events import add_event
from models.users import add_user
from storage import load_events, load_users, save_events, save_users


def test_users_roundtrip(tmp_path):
    users = []
    add_user(users, "Иван Петров", "ivan@example.com", "participant")
    filename = tmp_path / "users.json"
    save_users(str(filename), users)
    loaded = load_users(str(filename))
    assert len(loaded) == 1
    assert loaded[0].email == "ivan@example.com"
    assert str(loaded[0].id) == "1"


def test_events_roundtrip(tmp_path):
    events = []
    add_event(
        events,
        "Python для начинающих",
        date(2026, 10, 15),
        "Курс",
        60,
    )
    filename = tmp_path / "events.json"
    save_events(str(filename), events)
    loaded = load_events(str(filename))
    assert loaded[0].title == "Python для начинающих"
    assert loaded[0].date == date(2026, 10, 15)
    assert loaded[0].is_score_enough(60)


def test_missing_file_returns_empty(tmp_path):
    loaded = load_users(str(tmp_path / "missing.json"))
    assert loaded == []
