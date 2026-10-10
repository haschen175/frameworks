"""Мероприятия, по итогам которых выдаются сертификаты."""

from datetime import date, datetime


class Event:
    """Мероприятие: курс, семинар, олимпиада."""

    def __init__(
        self,
        event_id: int,
        title: str,
        event_date: date,
        description: str = "",
        min_score: float = 60.0,
    ) -> None:
        """Сохранить данные мероприятия."""
        self.id = event_id
        self.title = title
        self.date = event_date
        self.description = description
        self.min_score = float(min_score)

    def __str__(self) -> str:
        """Вернуть краткое описание мероприятия."""
        return (
            f"{self.title} ({self.date:%Y-%m-%d}), "
            f"проходной балл {self.min_score}"
        )

    def is_score_enough(self, score: float) -> bool:
        """Проверить, достаточен ли балл для зачёта."""
        return float(score) >= self.min_score

    @staticmethod
    def validate_min_score(min_score: float) -> bool:
        """Проверить, что проходной балл не отрицательный."""
        return float(min_score) >= 0

    @classmethod
    def from_data(cls, data: dict) -> "Event":
        """Создать мероприятие из словаря JSON."""
        raw_date = str(data["date"])
        event_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        return cls(
            event_id=int(data["id"]),
            title=str(data["title"]),
            event_date=event_date,
            description=str(data.get("description", "")),
            min_score=float(data.get("min_score", 60)),
        )

    def to_data(self) -> dict:
        """Преобразовать мероприятие в словарь для JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date.strftime("%Y-%m-%d"),
            "description": self.description,
            "min_score": self.min_score,
        }


def next_event_id(events: list[Event]) -> int:
    """Вернуть следующий свободный идентификатор."""
    if not events:
        return 1
    return max(event.id for event in events) + 1


def add_event(
    events: list[Event],
    title: str,
    event_date: date,
    description: str = "",
    min_score: float = 60.0,
) -> Event | None:
    """Добавить мероприятие в коллекцию."""
    if not title.strip():
        print("[ОШИБКА] Название мероприятия не задано.")
        return None
    if not Event.validate_min_score(min_score):
        print("[ОШИБКА] Проходной балл не может быть отрицательным.")
        return None
    event = Event(
        next_event_id(events),
        title.strip(),
        event_date,
        description,
        min_score,
    )
    events.append(event)
    print(f"[OK] Мероприятие создано: {event}")
    return event


def find_event(events: list[Event], query: str) -> list[Event]:
    """Найти мероприятия по подстроке названия."""
    needle = query.casefold()
    found: list[Event] = []
    for event in events:
        if needle in event.title.casefold():
            found.append(event)
    return found


def find_event_by_id(
    events: list[Event],
    event_id: int,
) -> Event | None:
    """Найти мероприятие по идентификатору."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def check_event_score(
    events: list[Event],
    event_id: int,
    score: float,
) -> bool:
    """Проверить, проходит ли балл порог мероприятия."""
    event = find_event_by_id(events, event_id)
    if event is None:
        return False
    return event.is_score_enough(score)


def iter_events_by_min_score(
    events: list[Event],
    min_score: float,
):
    """Генератор мероприятий с порогом не ниже заданного."""
    for event in events:
        if event.min_score >= min_score:
            yield event


def filter_events_by_min_score(
    events: list[Event],
    min_score: float,
) -> list[Event]:
    """Отобрать мероприятия по проходному баллу."""
    return list(iter_events_by_min_score(events, min_score))


def sort_events(
    events: list[Event],
    by: str = "date",
) -> list[Event]:
    """Вернуть мероприятия, упорядоченные по дате или названию."""
    if by == "title":
        return sorted(events, key=lambda event: event.title.casefold())
    return sorted(events, key=lambda event: event.date)
