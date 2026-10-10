"""Консольный интерфейс сервиса выдачи электронных сертификатов."""

from models.certificates import (
    get_certificate_status,
    get_certificates_by_user,
    issue_certificate,
    revoke_certificate,
)
from models.events import (
    add_event,
    check_event_score,
    filter_events_by_min_score,
    find_event,
    find_event_by_id,
    sort_events,
)
from models.results import add_result, find_result_by_id, iter_passed_results
from models.users import add_user, delete_user, find_user_by_id, update_user
from storage import (
    load_certificates,
    load_events,
    load_results,
    load_users,
    save_certificates,
    save_events,
    save_results,
    save_users,
)
from utils import (
    describe_callable,
    format_score,
    input_date,
    input_float,
    input_int,
    input_non_empty,
)

USERS_FILE = "data/users.json"
EVENTS_FILE = "data/events.json"
RESULTS_FILE = "data/results.json"
CERTIFICATES_FILE = "data/certificates.json"


def show_users(users) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователей нет.")
        return
    for number in range(1, len(users) + 1):
        print(f"  {number}. {users[number - 1]}")


def show_events(events) -> None:
    """Вывести список мероприятий."""
    if not events:
        print("Мероприятий нет.")
        return
    ordered = sort_events(events)
    for event in ordered:
        print(f"  id={event.id}: {event}")
        if event.description:
            print(f"     {event.description}")


def show_results(results) -> None:
    """Вывести список результатов."""
    if not results:
        print("Результатов нет.")
        return
    for result in results:
        print(f"  {result}")


def show_certificates(certificates) -> None:
    """Вывести список сертификатов и их статус."""
    if not certificates:
        print("Сертификатов нет.")
        return
    for certificate in certificates:
        status = get_certificate_status(certificate.is_active)
        print(f"  {certificate} — {status}")


def print_statistics(users, events, results, certificates) -> None:
    """Вывести сводную статистику системы."""
    total_results = len(results)
    passed_count = sum(1 for _ in iter_passed_results(results))
    failed_count = total_results - passed_count
    if total_results > 0:
        pass_rate = round(passed_count / total_results * 100, 1)
    else:
        pass_rate = 0.0
    active = sum(1 for item in certificates if item.is_active)
    print("=" * 50)
    print("СТАТИСТИКА")
    print(f"  Пользователей : {len(users)}")
    print(f"  Мероприятий   : {len(events)}")
    print(f"  Результатов   : {total_results}")
    print(f"    зачтено     : {passed_count}")
    print(f"    не зачтено  : {failed_count}")
    print(f"    процент     : {format_score(pass_rate)}")
    print(f"  Сертификатов  : {len(certificates)} (действуют: {active})")
    print("=" * 50)


def save_all(users, events, results, certificates) -> None:
    """Сохранить все коллекции проекта."""
    save_users(USERS_FILE, users)
    save_events(EVENTS_FILE, events)
    save_results(RESULTS_FILE, results)
    save_certificates(CERTIFICATES_FILE, certificates)


def load_all():
    """Загрузить данные проекта и связать объекты."""
    users = load_users(USERS_FILE)
    events = load_events(EVENTS_FILE)
    results = load_results(RESULTS_FILE, users, events)
    certificates = load_certificates(
        CERTIFICATES_FILE,
        users,
        events,
        results,
    )
    return users, events, results, certificates


def handle_find_event(events) -> None:
    """Пункт меню: поиск мероприятия по названию."""
    query = input_non_empty("Часть названия: ")
    found = find_event(events, query)
    if not found:
        print("Ничего не найдено.")
        return
    show_events(found)


def handle_check_score(events) -> None:
    """Пункт меню: проверка балла относительно порога."""
    event_id = input_int("ID мероприятия: ")
    score = input_float("Балл участника: ")
    event = find_event_by_id(events, event_id)
    if event is None:
        print("[ОШИБКА] Мероприятие не найдено.")
        return
    passed = check_event_score(events, event_id, score)
    if passed:
        print(
            f"Балл {format_score(score)} достаточен "
            f"для «{event.title}»."
        )
    else:
        print(
            f"Балл {format_score(score)} ниже порога "
            f"{format_score(event.min_score)}."
        )


def handle_add_user(users) -> None:
    """Пункт меню: регистрация пользователя."""
    full_name = input_non_empty("ФИО: ")
    email = input_non_empty("Email: ")
    role = input("Роль (participant/organizer) [participant]: ").strip()
    if not role:
        role = "participant"
    if add_user(users, full_name, email, role) is not None:
        save_users(USERS_FILE, users)


def handle_add_event(events) -> None:
    """Пункт меню: создание мероприятия."""
    title = input_non_empty("Название: ")
    event_date = input_date("Дата: ")
    description = input("Описание: ").strip()
    min_score = input_float("Проходной балл: ")
    if add_event(events, title, event_date, description, min_score):
        save_events(EVENTS_FILE, events)


def handle_add_result(users, events, results) -> None:
    """Пункт меню: фиксация результата участия."""
    user = find_user_by_id(users, input_int("ID пользователя: "))
    event = find_event_by_id(events, input_int("ID мероприятия: "))
    if user is None or event is None:
        print("[ОШИБКА] Пользователь или мероприятие не найдены.")
        return
    score = input_float("Балл: ")
    add_result(results, user, event, score)
    save_results(RESULTS_FILE, results)


def handle_issue(results, certificates) -> None:
    """Пункт меню: выдача сертификата по результату."""
    result = find_result_by_id(results, input_int("ID результата: "))
    if result is None:
        print("[ОШИБКА] Результат не найден.")
        return
    before = len(certificates)
    issue_certificate(certificates, result)
    if len(certificates) != before:
        save_certificates(CERTIFICATES_FILE, certificates)


def handle_revoke(certificates) -> None:
    """Пункт меню: аннулирование сертификата."""
    certificate_id = input_int("ID сертификата: ")
    if revoke_certificate(certificates, certificate_id):
        save_certificates(CERTIFICATES_FILE, certificates)


def handle_by_user(users, certificates) -> None:
    """Пункт меню: сертификаты одного пользователя."""
    user_id = input_int("ID пользователя: ")
    user = find_user_by_id(users, user_id)
    if user is None:
        print("[ОШИБКА] Пользователь не найден.")
        return
    selected = get_certificates_by_user(certificates, user_id)
    print(f"Сертификаты пользователя {user.full_name}:")
    show_certificates(selected)


def handle_filter(events) -> None:
    """Пункт меню: отбор мероприятий по проходному баллу."""
    min_score = input_float("Минимальный проходной балл: ")
    selected = filter_events_by_min_score(events, min_score)
    show_events(selected)


def handle_update_user(users) -> None:
    """Пункт меню: изменение ФИО пользователя."""
    user_id = input_int("ID пользователя: ")
    full_name = input_non_empty("Новое ФИО: ")
    if update_user(users, user_id, full_name=full_name):
        save_users(USERS_FILE, users)


def handle_delete_user(users) -> None:
    """Пункт меню: удаление пользователя."""
    user_id = input_int("ID пользователя: ")
    if delete_user(users, user_id):
        save_users(USERS_FILE, users)


def show_help() -> None:
    """Показать документацию ключевой функции через интроспекцию."""
    print(describe_callable(issue_certificate))
    print(describe_callable(get_certificate_status))


def print_menu() -> None:
    """Вывести пункты меню."""
    print()
    print("=== Сервис выдачи электронных сертификатов ===")
    items = (
        "Показать мероприятия",
        "Найти мероприятие по названию",
        "Проверить балл относительно порога",
        "Отобрать мероприятия по проходному баллу",
        "Показать пользователей",
        "Добавить пользователя",
        "Изменить ФИО пользователя",
        "Удалить пользователя",
        "Добавить мероприятие",
        "Добавить результат",
        "Показать результаты",
        "Выдать сертификат",
        "Аннулировать сертификат",
        "Показать сертификаты",
        "Сертификаты пользователя",
        "Статистика",
        "Справка (интроспекция)",
    )
    for index, title in enumerate(items, start=1):
        print(f"{index}. {title}")
    print("0. Выход")


def main() -> None:
    """Точка запуска: меню и вызов функций проекта."""
    users, events, results, certificates = load_all()
    actions = {
        1: lambda: show_events(events),
        2: lambda: handle_find_event(events),
        3: lambda: handle_check_score(events),
        4: lambda: handle_filter(events),
        5: lambda: show_users(users),
        6: lambda: handle_add_user(users),
        7: lambda: handle_update_user(users),
        8: lambda: handle_delete_user(users),
        9: lambda: handle_add_event(events),
        10: lambda: handle_add_result(users, events, results),
        11: lambda: show_results(results),
        12: lambda: handle_issue(results, certificates),
        13: lambda: handle_revoke(certificates),
        14: lambda: show_certificates(certificates),
        15: lambda: handle_by_user(users, certificates),
        16: lambda: print_statistics(
            users, events, results, certificates
        ),
        17: show_help,
    }
    while True:
        print_menu()
        choice = input_int("Выберите действие: ")
        if choice == 0:
            save_all(users, events, results, certificates)
            print("Программа завершена. Данные сохранены.")
            break
        action = actions.get(choice)
        if action is None:
            print("[ОШИБКА] Нет такого пункта меню.")
            continue
        action()


if __name__ == "__main__":
    main()
