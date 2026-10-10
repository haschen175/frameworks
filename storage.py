"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
from pathlib import Path

from models.certificates import Certificate
from models.events import Event
from models.results import Result
from models.users import User

BASE_DIR = Path(__file__).resolve().parent


def resolve_path(filename: str) -> Path:
    """Преобразовать путь к файлу данных относительно корня проекта."""
    path = Path(filename)
    if path.is_absolute():
        return path
    return BASE_DIR / path


def read_json(filename: str) -> list:
    """Прочитать список из JSON-файла.

    Отсутствие файла и повреждённый JSON не останавливают программу.
    """
    path = resolve_path(filename)
    try:
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"[ОШИБКА] Файл не найден: {path}. Будет создан пустой список.")
        return []
    except json.JSONDecodeError:
        print(f"[ОШИБКА] Некорректный JSON: {path}.")
        return []
    if not isinstance(data, list):
        print(f"[ОШИБКА] В файле {path} ожидается список.")
        return []
    return data


def write_json(filename: str, rows: list) -> None:
    """Записать список словарей в JSON-файл."""
    path = resolve_path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)


def load_users(filename: str) -> list[User]:
    """Загрузить пользователей из JSON-файла."""
    users: list[User] = []
    for row in read_json(filename):
        try:
            users.append(User.from_data(row))
        except (KeyError, TypeError, ValueError) as error:
            print(f"[ОШИБКА] Пропуск пользователя: {error}")
    return users


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить пользователей в JSON-файл."""
    write_json(filename, [user.to_data() for user in users])


def load_events(filename: str) -> list[Event]:
    """Загрузить мероприятия из JSON-файла."""
    events: list[Event] = []
    for row in read_json(filename):
        try:
            events.append(Event.from_data(row))
        except (KeyError, TypeError, ValueError) as error:
            print(f"[ОШИБКА] Пропуск мероприятия: {error}")
    return events


def save_events(filename: str, events: list[Event]) -> None:
    """Сохранить мероприятия в JSON-файл."""
    write_json(filename, [event.to_data() for event in events])


def load_results(
    filename: str,
    users: list[User],
    events: list[Event],
) -> list[Result]:
    """Загрузить результаты и связать их с объектами."""
    results: list[Result] = []
    for row in read_json(filename):
        try:
            results.append(Result.from_data(row, users, events))
        except (KeyError, TypeError, ValueError) as error:
            print(f"[ОШИБКА] Пропуск результата: {error}")
    return results


def save_results(filename: str, results: list[Result]) -> None:
    """Сохранить результаты в JSON-файл."""
    write_json(filename, [result.to_data() for result in results])


def load_certificates(
    filename: str,
    users: list[User],
    events: list[Event],
    results: list[Result],
) -> list[Certificate]:
    """Загрузить сертификаты и восстановить связи объектов."""
    certificates: list[Certificate] = []
    for row in read_json(filename):
        try:
            certificates.append(
                Certificate.from_data(row, users, events, results)
            )
        except (KeyError, TypeError, ValueError) as error:
            print(f"[ОШИБКА] Пропуск сертификата: {error}")
    return certificates


def save_certificates(
    filename: str,
    certificates: list[Certificate],
) -> None:
    """Сохранить сертификаты в JSON-файл."""
    write_json(
        filename,
        [certificate.to_data() for certificate in certificates],
    )
