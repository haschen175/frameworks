#импорт
from services import (
    create_user,
    list_users,
    update_user,
    delete_user,
    create_event,
    list_events,
    add_result,
    list_results,
    issue_certificate,
    list_certificates,
    get_certificates_by_user,
    print_statistics,
)


def main() -> None:

    print("=" * 50)
    print("  СЕРВИС ВЫДАЧИ ЭЛЕКТРОННЫХ СЕРТИФИКАТОВ")
    print("=" * 50)

    #создание пользователей
    print("\n--- Регистрация пользователей ---")
    user1 = create_user("Иванов Иван Иванович", "ivanov@example.com", "participant")
    user2 = create_user("Петрова Мария Сергеевна", "petrova@example.com", "participant")
    user3 = create_user("Сидоров Алексей Петрович", "sidorov@example.com", "organizer")
    #попытка создать дубликат
    create_user("Дубль Иванов", "ivanov@example.com", "participant")

    #просмотр пользователей
    print("\n--- Все пользователи ---")
    for user in list_users():
        print(f"  {user}")

    #обновление пользователя 
    print("\n--- Обновление пользователя ---")
    update_user(user1.id, full_name="Иванов Иван Петрович")

    # создание мероприятий
    print("\n--- Создание мероприятий ---")
    event1 = create_event(
        title="Python для начинающих",
        date="2026-10-15",
        description="Вводный курс по программированию на Python",
        min_score=60,
    )
    event2 = create_event(
        title="Олимпиада по информатике",
        date="2026-11-20",
        description="Региональный этап олимпиады",
        min_score=75,
    )

    print("\n--- Все мероприятия ---")
    for event in list_events():
        print(f"  {event}")

    #добавление результатов
    print("\n--- Добавление результатов участия ---")
    result1 = add_result(user1.id, event1.id, score=85.5)  # зачёт
    result2 = add_result(user2.id, event1.id, score=45.0)  # не зачтено
    result3 = add_result(user1.id, event2.id, score=90.0)  # зачёт
    result4 = add_result(user2.id, event2.id, score=78.0)  # зачёт

    print("\n--- Все результаты ---")
    for result in list_results():
        status: str = "[+] ЗАЧЁТ" if result.passed else "[-] не зачтено"
        print(f"  {result}  --  {status}")

    # выдача сертификатов
    print("\n--- Выдача сертификатов ---")
    issue_certificate(result1.id)  # успех
    issue_certificate(result2.id)  # отказ не зачтено
    issue_certificate(result3.id)  # успех
    issue_certificate(result4.id)  # успех
    #повторная попытка сертификат уже выдан
    issue_certificate(result1.id)

    #просмотр сертификатов
    print("\n--- Все сертификаты ---")
    for cert in list_certificates():
        print(f"  {cert}")

    # фильтрация по пользователю
    print(f"\n--- Сертификаты пользователя '{user1.full_name}' ---")
    for cert in get_certificates_by_user(user1.id):
        print(f"  {cert}")

    # удаление пользователя 
    print("\n--- Удаление пользователя ---")
    delete_user(user3.id)
    print("\n--- Пользователи после удаления ---")
    for user in list_users():
        print(f"  {user}")

    #статистика 
    print_statistics()

    print("\nПрограмма завершена.")


#точка входа
if __name__ == "__main__":
    main()
