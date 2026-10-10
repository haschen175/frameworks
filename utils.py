"""Вспомогательные функции ввода и интроспекции."""

import inspect
from datetime import datetime


def format_score(score: float) -> str:
    """Отформатировать балл.

    Вложенная функция показывает локальную область видимости:
    снаружи модуля к round_part обратиться нельзя.
    """

    def round_part(value: float) -> str:
        return f"{value:.1f}"

    return round_part(score)


def describe_callable(func) -> str:
    """Показать сигнатуру и документацию функции (интроспекция)."""
    signature = inspect.signature(func)
    document = inspect.getdoc(func) or "нет описания"
    return f"{func.__name__}{signature}\n{document}"


def input_int(prompt: str) -> int:
    """Запросить целое число. При ошибке запрос повторяется."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("[ОШИБКА] Введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить число. При ошибке запрос повторяется."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("[ОШИБКА] Введите число.")


def input_date(prompt: str):
    """Запросить дату. Допустимы форматы ГГГГ-ММ-ДД и ДД.ММ.ГГГГ."""
    while True:
        raw = input(prompt).strip()
        for pattern in ("%Y-%m-%d", "%d.%m.%Y"):
            try:
                return datetime.strptime(raw, pattern).date()
            except ValueError:
                continue
        print("[ОШИБКА] Введите дату как 2026-10-15 или 15.10.2026.")


def input_non_empty(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("[ОШИБКА] Строка не должна быть пустой.")
