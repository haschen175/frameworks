"""Результаты участия пользователей в мероприятиях."""

from models.events import Event, find_event_by_id
from models.users import User, find_user_by_id


class Result:
    """Результат участия: баллы и признак зачёта."""

    def __init__(
        self,
        result_id: int,
        user: User,
        event: Event,
        score: float,
    ) -> None:
        """Сохранить результат и вычислить статус зачёта."""
        self.id = result_id
        self.user = user
        self.event = event
        self.score = float(score)
        self.passed = event.is_score_enough(self.score)

    def __str__(self) -> str:
        """Вернуть краткое описание результата."""
        status = "зачёт" if self.passed else "не зачтено"
        return (
            f"Результат #{self.id}: {self.user.full_name}, "
            f"{self.event.title}, {self.score} ({status})"
        )

    @classmethod
    def from_data(
        cls,
        data: dict,
        users: list[User],
        events: list[Event],
    ) -> "Result":
        """Создать результат из словаря JSON и связанных объектов."""
        user = find_user_by_id(users, int(data["user_id"]))
        event = find_event_by_id(events, int(data["event_id"]))
        if user is None or event is None:
            raise ValueError(
                "для результата не найдены пользователь или мероприятие"
            )
        return cls(
            result_id=int(data["id"]),
            user=user,
            event=event,
            score=float(data["score"]),
        )

    def to_data(self) -> dict:
        """Преобразовать результат в словарь для JSON."""
        return {
            "id": self.id,
            "user_id": self.user.id,
            "event_id": self.event.id,
            "score": self.score,
            "passed": self.passed,
        }


def next_result_id(results: list[Result]) -> int:
    """Вернуть следующий свободный идентификатор."""
    if not results:
        return 1
    return max(item.id for item in results) + 1


def add_result(
    results: list[Result],
    user: User,
    event: Event,
    score: float,
) -> Result:
    """Добавить результат участия и определить зачёт."""
    result = Result(next_result_id(results), user, event, score)
    results.append(result)
    if result.passed:
        print(
            f"[OK] Результат добавлен: {result}. "
            f"Балл {result.score} >= {event.min_score}."
        )
    else:
        print(
            f"[OK] Результат добавлен: {result}. "
            f"Балл {result.score} < {event.min_score}."
        )
    return result


def find_result_by_id(
    results: list[Result],
    result_id: int,
) -> Result | None:
    """Найти результат по идентификатору."""
    for result in results:
        if result.id == result_id:
            return result
    return None


def iter_passed_results(results: list[Result]):
    """Генератор результатов со статусом «зачёт»."""
    for result in results:
        if result.passed:
            yield result
