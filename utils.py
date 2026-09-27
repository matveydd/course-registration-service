"""Вспомогательные функции ввода с обработкой некорректных данных."""

from datetime import date


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число, повторяя запрос при ошибке."""
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Нужно ввести целое число, попробуйте ещё раз.")


def input_nonempty(prompt: str) -> str:
    """Запросить у пользователя непустую строку."""
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Значение не может быть пустым, попробуйте ещё раз.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        raw = input(prompt)
        try:
            day_str, month_str, year_str = raw.split(".")
            return date(int(year_str), int(month_str), int(day_str))
        except ValueError:
            print(
                "Нужно ввести дату в формате ДД.ММ.ГГГГ, попробуйте ещё раз."
            )
