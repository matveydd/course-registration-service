"""Класс Result и функции для работы с результатами прохождения курсов."""

from datetime import date

from models.applications import Application, find_application_by_id


class Result:
    """Результат прохождения курса по заявке."""

    def __init__(
        self, application: Application, score: int, completed_at: str
    ) -> None:
        """Создать объект результата."""
        self.application = application
        self.score = score
        self.completed_at = completed_at

    def evaluate(self) -> str:
        """Вернуть текстовую оценку результата по количеству баллов."""
        if self.score >= 90:
            return "высокий балл"
        if self.score >= 50:
            return "средний балл"
        return "низкий балл"

    def __str__(self) -> str:
        """Вернуть строковое представление результата."""
        return (
            f"{self.score} баллов ({self.evaluate()}), "
            f"завершено {self.completed_at}"
        )


def find_result_for_application(
    results: list[Result], application_id: int
) -> Result | None:
    """Найти результат по идентификатору заявки, если он есть."""
    for result in results:
        if result.application.id == application_id:
            return result
    return None


def record_result(
    applications: list[Application],
    results: list[Result],
    application_id: int,
    score: int,
    completed_at: date,
) -> Result:
    """Зафиксировать результат для одобренной заявки.

    Вызывает ValueError, если заявка не найдена, не одобрена или
    результат по ней уже зафиксирован.
    """
    application = find_application_by_id(applications, application_id)
    if application is None:
        raise ValueError(f"Заявка с id={application_id} не найдена")
    if application.status != "approved":
        raise ValueError(
            "Результат можно зафиксировать только для одобренной заявки"
        )
    if find_result_for_application(results, application_id) is not None:
        raise ValueError("Результат по этой заявке уже зафиксирован")

    result = Result(application, score, completed_at.isoformat())
    results.append(result)
    return result
