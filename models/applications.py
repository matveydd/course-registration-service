"""Класс Application и функции для работы с заявками на курсы."""

from typing import TYPE_CHECKING

from models.courses import Course, is_course_available

if TYPE_CHECKING:
    from models.employees import Employee


class Application:
    """Заявка сотрудника на курс."""

    def __init__(
        self,
        application_id: int,
        employee: "Employee",
        course: Course,
        status: str = "pending",
        rejection_reason: str | None = None,
        history: list[dict] | None = None,
    ) -> None:
        """Создать объект заявки."""
        self.id = application_id
        self.employee = employee
        self.course = course
        self.status = status
        self.rejection_reason = rejection_reason
        self.history = (
            history if history is not None else [{"from": None, "to": status}]
        )

    def approve(self) -> None:
        """Одобрить заявку."""
        self.history.append({"from": self.status, "to": "approved"})
        self.status = "approved"

    def reject(self, reason: str) -> None:
        """Отклонить заявку с указанием причины."""
        self.history.append({"from": self.status, "to": "rejected"})
        self.status = "rejected"
        self.rejection_reason = reason

    def cancel(self) -> None:
        """Отменить заявку, не удаляя её из истории."""
        self.history.append({"from": self.status, "to": "cancelled"})
        self.status = "cancelled"

    def __str__(self) -> str:
        """Вернуть строковое представление заявки."""
        return (
            f"Заявка №{self.id}: {self.employee.full_name} → "
            f"«{self.course.title}» [{self.status}]"
        )


def find_application_by_id(
    applications: list[Application], application_id: int
) -> Application | None:
    """Найти заявку по идентификатору."""
    for application in applications:
        if application.id == application_id:
            return application
    return None


def find_applications_by_employee(
    applications: list[Application], employee: "Employee"
) -> list[Application]:
    """Найти все заявки конкретного сотрудника."""
    return [a for a in applications if a.employee is employee]


def has_active_application(
    applications: list[Application], employee: "Employee", course: Course
) -> bool:
    """Проверить, есть ли у сотрудника действующая заявка на этот курс."""
    return any(
        a.employee is employee
        and a.course is course
        and a.status in ("pending", "approved")
        for a in applications
    )


def create_application(
    applications: list[Application], employee: "Employee", course: Course
) -> Application:
    """Создать заявку на курс.

    Вызывает ValueError, если мест нет или у сотрудника уже есть
    действующая заявка на этот курс.
    """
    if has_active_application(applications, employee, course):
        raise ValueError("Заявка на этот курс уже подана")
    if not is_course_available(applications, course):
        raise ValueError("На курсе нет свободных мест")

    application_id = max((a.id for a in applications), default=0) + 1
    application = Application(application_id, employee, course)
    applications.append(application)
    return application


def approve_application(
    applications: list[Application], application_id: int
) -> None:
    """Одобрить заявку с проверкой лимита мест на курсе."""
    application = find_application_by_id(applications, application_id)
    if application is None:
        raise ValueError(f"Заявка с id={application_id} не найдена")
    if application.status != "pending":
        raise ValueError(
            "Одобрить можно только заявку в статусе «на рассмотрении»"
        )
    if not is_course_available(applications, application.course):
        raise ValueError("На курсе нет свободных мест")
    application.approve()


def reject_application(
    applications: list[Application], application_id: int, reason: str
) -> None:
    """Отклонить заявку с указанием причины."""
    application = find_application_by_id(applications, application_id)
    if application is None:
        raise ValueError(f"Заявка с id={application_id} не найдена")
    if application.status != "pending":
        raise ValueError(
            "Отклонить можно только заявку в статусе «на рассмотрении»"
        )
    application.reject(reason)


def cancel_application(
    applications: list[Application], application_id: int
) -> None:
    """Отменить заявку, пока она ещё не рассмотрена."""
    application = find_application_by_id(applications, application_id)
    if application is None:
        raise ValueError(f"Заявка с id={application_id} не найдена")
    if application.status != "pending":
        raise ValueError(
            "Отменить можно только заявку в статусе «на рассмотрении»"
        )
    application.cancel()


def get_application_status(application: Application) -> str:
    """Вернуть текстовое описание статуса заявки."""
    if application.status == "pending":
        return "Заявка принята к рассмотрению"
    if application.status == "approved":
        return "Заявка одобрена"
    if application.status == "rejected":
        return f"Заявка отклонена: {application.rejection_reason}"
    if application.status == "cancelled":
        return "Заявка отменена"
    return "Неизвестный статус заявки"
