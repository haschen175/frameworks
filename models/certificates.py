"""Электронные сертификаты по зачтённым результатам."""

from datetime import datetime

from models.events import Event, find_event_by_id
from models.results import Result, find_result_by_id
from models.users import User, find_user_by_id


class Certificate:
    """Сертификат, подтверждающий зачтённый результат."""

    def __init__(
        self,
        certificate_id: int,
        user: User,
        event: Event,
        result: Result,
        issued_at: datetime | None = None,
        number: str | None = None,
        is_revoked: bool = False,
    ) -> None:
        """Сохранить связи сертификата и сформировать номер."""
        self.id = certificate_id
        self.user = user
        self.event = event
        self.result = result
        self.issued_at = issued_at or datetime.now()
        self.number = number or self.build_number(
            certificate_id,
            self.issued_at,
        )
        self.is_revoked = is_revoked

    def __str__(self) -> str:
        """Вернуть краткое описание сертификата."""
        return (
            f"{self.number}: {self.user.full_name}, {self.event.title}"
        )

    @property
    def is_active(self) -> bool:
        """Сертификат действует, пока его не аннулировали."""
        return not self.is_revoked

    @staticmethod
    def build_number(certificate_id: int, issued_at: datetime) -> str:
        """Собрать уникальный номер сертификата."""
        return f"CERT-{issued_at:%Y%m%d}-{certificate_id:04d}"

    def revoke(self) -> None:
        """Аннулировать сертификат."""
        self.is_revoked = True

    @classmethod
    def from_data(
        cls,
        data: dict,
        users: list[User],
        events: list[Event],
        results: list[Result],
    ) -> "Certificate":
        """Создать сертификат из словаря JSON."""
        user = find_user_by_id(users, int(data["user_id"]))
        event = find_event_by_id(events, int(data["event_id"]))
        result = find_result_by_id(results, int(data["result_id"]))
        if user is None or event is None or result is None:
            raise ValueError(
                "для сертификата не найдены связанные объекты"
            )
        issued_raw = data.get("issued_at")
        issued_at = None
        if issued_raw:
            issued_at = datetime.fromisoformat(str(issued_raw))
        return cls(
            certificate_id=int(data["id"]),
            user=user,
            event=event,
            result=result,
            issued_at=issued_at,
            number=data.get("number"),
            is_revoked=bool(data.get("is_revoked", False)),
        )

    def to_data(self) -> dict:
        """Преобразовать сертификат в словарь для JSON."""
        return {
            "id": self.id,
            "user_id": self.user.id,
            "event_id": self.event.id,
            "result_id": self.result.id,
            "number": self.number,
            "issued_at": self.issued_at.isoformat(timespec="seconds"),
            "is_revoked": self.is_revoked,
        }


def get_certificate_status(is_active: bool) -> str:
    """Вернуть текстовый статус сертификата.

    Функция сохраняет сценарий ПР1: по логическому признаку
    возвращается понятная пользователю строка.
    """
    if is_active:
        return "Сертификат действует"
    return "Сертификат аннулирован"


def next_certificate_id(certificates: list[Certificate]) -> int:
    """Вернуть следующий свободный идентификатор."""
    if not certificates:
        return 1
    return max(item.id for item in certificates) + 1


def find_certificate_by_id(
    certificates: list[Certificate],
    certificate_id: int,
) -> Certificate | None:
    """Найти сертификат по идентификатору."""
    for certificate in certificates:
        if certificate.id == certificate_id:
            return certificate
    return None


def find_certificate_by_result(
    certificates: list[Certificate],
    result_id: int,
) -> Certificate | None:
    """Найти сертификат, уже выданный по результату."""
    for certificate in certificates:
        if certificate.result.id == result_id:
            return certificate
    return None


def issue_certificate(
    certificates: list[Certificate],
    result: Result,
) -> Certificate | None:
    """Выдать сертификат, если результат зачтён и ещё не выдан."""
    if not result.passed:
        print(
            "[ОТКАЗ] Сертификат не выдан: "
            f"результат id={result.id} не зачтён "
            f"(score={result.score})."
        )
        return None
    existing = find_certificate_by_result(certificates, result.id)
    if existing is not None:
        print(
            "[ОШИБКА] Сертификат для результата "
            f"id={result.id} уже выдан: {existing}"
        )
        return existing
    certificate = Certificate(
        next_certificate_id(certificates),
        result.user,
        result.event,
        result,
    )
    certificates.append(certificate)
    print(f"[OK] Сертификат выдан: {certificate}")
    return certificate


def revoke_certificate(
    certificates: list[Certificate],
    certificate_id: int,
) -> bool:
    """Аннулировать сертификат по идентификатору."""
    certificate = find_certificate_by_id(certificates, certificate_id)
    if certificate is None:
        print(f"[ОШИБКА] Сертификат id={certificate_id} не найден.")
        return False
    if certificate.is_revoked:
        print(f"[ОШИБКА] Сертификат уже аннулирован: {certificate}")
        return False
    certificate.revoke()
    print(f"[OK] Сертификат аннулирован: {certificate}")
    return True


def get_certificates_by_user(
    certificates: list[Certificate],
    user_id: int,
) -> list[Certificate]:
    """Вернуть сертификаты конкретного пользователя."""
    return [
        item for item in certificates if item.user.id == user_id
    ]


def get_certificates_by_event(
    certificates: list[Certificate],
    event_id: int,
) -> list[Certificate]:
    """Вернуть сертификаты конкретного мероприятия."""
    return [
        item for item in certificates if item.event.id == event_id
    ]
