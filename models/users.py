"""Пользователи сервиса выдачи сертификатов."""


class User:
    """Пользователь системы: участник или организатор."""

    def __init__(
        self,
        user_id: int,
        full_name: str,
        email: str,
        role: str = "participant",
    ) -> None:
        """Сохранить данные пользователя в атрибутах объекта."""
        self.id = user_id
        self.full_name = full_name
        self.email = email
        self.role = role

    def __str__(self) -> str:
        """Вернуть удобное описание пользователя."""
        return (
            f"{self.full_name} <{self.email}>, роль: {self.role}"
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверить, что строка похожа на адрес электронной почты."""
        if "@" not in email:
            return False
        name, domain = email.split("@", 1)
        return bool(name) and "." in domain

    @staticmethod
    def validate_role(role: str) -> bool:
        """Проверить допустимую роль пользователя."""
        allowed = ("participant", "organizer")
        return role in allowed

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря JSON."""
        return cls(
            user_id=int(data["id"]),
            full_name=str(data["full_name"]),
            email=str(data["email"]),
            role=str(data.get("role", "participant")),
        )

    def to_data(self) -> dict:
        """Преобразовать пользователя в словарь для JSON."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
        }


def next_user_id(users: list[User]) -> int:
    """Вернуть следующий свободный идентификатор."""
    if not users:
        return 1
    return max(user.id for user in users) + 1


def add_user(
    users: list[User],
    full_name: str,
    email: str,
    role: str = "participant",
) -> User | None:
    """Добавить пользователя в коллекцию.

    Повторный email не создаёт второго объекта.
    """
    emails = {user.email for user in users}
    if email in emails:
        print(f"[ОШИБКА] Пользователь с email '{email}' уже есть.")
        return None
    if not User.validate_email(email):
        print(f"[ОШИБКА] Некорректный email: {email}")
        return None
    if not User.validate_role(role):
        print(f"[ОШИБКА] Некорректная роль: {role}")
        return None
    user = User(next_user_id(users), full_name, email, role)
    users.append(user)
    print(f"[OK] Пользователь создан: {user}")
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Найти пользователей по части ФИО или email."""
    needle = query.casefold()
    found: list[User] = []
    for user in users:
        full_name = user.full_name.casefold()
        email = user.email.casefold()
        if needle in full_name or needle in email:
            found.append(user)
    return found


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def update_user(
    users: list[User],
    user_id: int,
    full_name: str | None = None,
    role: str | None = None,
) -> bool:
    """Обновить ФИО или роль пользователя."""
    user = find_user_by_id(users, user_id)
    if user is None:
        print(f"[ОШИБКА] Пользователь id={user_id} не найден.")
        return False
    if full_name is not None:
        user.full_name = full_name
    if role is not None:
        if not User.validate_role(role):
            print(f"[ОШИБКА] Некорректная роль: {role}")
            return False
        user.role = role
    print(f"[OK] Пользователь обновлён: {user}")
    return True


def delete_user(users: list[User], user_id: int) -> bool:
    """Удалить пользователя по идентификатору."""
    user = find_user_by_id(users, user_id)
    if user is None:
        print(f"[ОШИБКА] Пользователь id={user_id} не найден.")
        return False
    users.remove(user)
    print(f"[OK] Пользователь удалён: {user}")
    return True
