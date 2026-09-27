"""Функции фиксации и просмотра результатов прохождения курсов."""

from datetime import date

from applications import find_application
from storage import load_json, save_json

RESULTS_FILE = "results.json"


def load_results() -> list[dict]:
    """Загрузить результаты из файла."""
    return load_json(RESULTS_FILE, default=[])


def save_results(results: list[dict]) -> None:
    """Сохранить результаты в файл."""
    save_json(RESULTS_FILE, results)


def has_result(results: list[dict], application_id: int) -> bool:
    """Проверить, зафиксирован ли уже результат по заявке."""
    return any(r["application_id"] == application_id for r in results)


def record_result(
    applications: list[dict],
    results: list[dict],
    application_id: int,
    score: int,
    completed_at: date,
) -> dict:
    """Зафиксировать результат для одобренной заявки.

    Вызывает ValueError, если заявка не одобрена или результат уже есть.
    """
    application = find_application(applications, application_id)
    if application["status"] != "approved":
        raise ValueError(
            "Результат можно зафиксировать только для одобренной заявки"
        )
    if has_result(results, application_id):
        raise ValueError("Результат по этой заявке уже зафиксирован")

    result = {
        "application_id": application_id,
        "score": score,
        "completed_at": completed_at.isoformat(),
    }
    results.append(result)
    return result


def get_result_for_application(
    results: list[dict], application_id: int
) -> dict | None:
    """Найти результат по идентификатору заявки, если он есть."""
    for result in results:
        if result["application_id"] == application_id:
            return result
    return None


def evaluate_result(score: int) -> str:
    """Вернуть текстовую оценку результата по количеству набранных баллов."""
    if score >= 90:
        return f"Результат: {score} баллов — высокий балл"
    if score >= 50:
        return f"Результат: {score} баллов — средний балл"
    return f"Результат: {score} баллов — низкий балл"
