"""Функции для создания заявок на курсы и работы с ними."""

from courses import is_course_available
from storage import load_json, save_json

APPLICATIONS_FILE = "applications.json"


def load_applications() -> list[dict]:
    """Загрузить заявки из файла."""
    return load_json(APPLICATIONS_FILE, default=[])


def save_applications(applications: list[dict]) -> None:
    """Сохранить заявки в файл."""
    save_json(APPLICATIONS_FILE, applications)


def find_application(applications: list[dict], application_id: int) -> dict:
    """Найти заявку по идентификатору.

    Вызывает ValueError, если заявка с таким идентификатором не найдена.
    """
    for application in applications:
        if application["id"] == application_id:
            return application
    raise ValueError(f"Заявка с id={application_id} не найдена")


def has_pending_or_approved_application(
    applications: list[dict], employee_id: int, course_id: int
) -> bool:
    """Проверить, есть ли у сотрудника действующая заявка на этот курс."""
    return any(
        application["employee_id"] == employee_id
        and application["course_id"] == course_id
        and application["status"] in ("pending", "approved")
        for application in applications
    )


def create_application(
    courses: dict[int, dict],
    applications: list[dict],
    employee_id: int,
    course_id: int,
) -> dict:
    """Создать заявку на курс.

    Вызывает ValueError, если курс не найден, мест нет или у сотрудника
    уже есть действующая заявка на этот курс.
    """
    if course_id not in courses:
        raise ValueError("Курс с таким идентификатором не найден")
    if has_pending_or_approved_application(
        applications, employee_id, course_id
    ):
        raise ValueError("Заявка на этот курс уже подана")
    if not is_course_available(courses, applications, course_id):
        raise ValueError("На курсе нет свободных мест")

    application = {
        "id": max((a["id"] for a in applications), default=0) + 1,
        "employee_id": employee_id,
        "course_id": course_id,
        "status": "pending",
        "rejection_reason": None,
        "history": [{"from": None, "to": "pending"}],
    }
    applications.append(application)
    return application


def approve_application(
    courses: dict[int, dict], applications: list[dict], application_id: int
) -> None:
    """Одобрить заявку с проверкой лимита мест на курсе."""
    application = find_application(applications, application_id)
    if application["status"] != "pending":
        raise ValueError(
            "Одобрить можно только заявку в статусе «на рассмотрении»"
        )
    if not is_course_available(
        courses, applications, application["course_id"]
    ):
        raise ValueError("На курсе нет свободных мест")

    application["history"].append(
        {"from": application["status"], "to": "approved"}
    )
    application["status"] = "approved"


def reject_application(
    applications: list[dict], application_id: int, reason: str
) -> None:
    """Отклонить заявку с указанием причины."""
    application = find_application(applications, application_id)
    if application["status"] != "pending":
        raise ValueError(
            "Отклонить можно только заявку в статусе «на рассмотрении»"
        )

    application["history"].append(
        {"from": application["status"], "to": "rejected"}
    )
    application["status"] = "rejected"
    application["rejection_reason"] = reason


def cancel_application(applications: list[dict], application_id: int) -> None:
    """Отменить заявку, пока она ещё не рассмотрена."""
    application = find_application(applications, application_id)
    if application["status"] != "pending":
        raise ValueError(
            "Отменить можно только заявку в статусе «на рассмотрении»"
        )
    applications.remove(application)


def find_applications_by_employee(
    applications: list[dict], employee_id: int
) -> list[dict]:
    """Найти все заявки конкретного сотрудника."""
    return [a for a in applications if a["employee_id"] == employee_id]


def get_application_status(application: dict) -> str:
    """Вернуть текстовое описание статуса заявки."""
    status = application["status"]
    if status == "pending":
        return "Заявка принята к рассмотрению"
    if status == "approved":
        return "Заявка одобрена"
    if status == "rejected":
        return f"Заявка отклонена: {application['rejection_reason']}"
    return "Неизвестный статус заявки"
