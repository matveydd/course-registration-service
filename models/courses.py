"""Класс Course и функции для работы с коллекцией курсов."""

from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.applications import Application


class Course:
    """Курс, доступный для подачи заявок."""

    def __init__(
        self, course_id: int, title: str, capacity: int, start_date: str
    ) -> None:
        """Создать объект курса."""
        self.id = course_id
        self.title = title
        self.capacity = capacity
        self.start_date = start_date

    def has_free_seats(self, taken: int) -> bool:
        """Проверить, есть ли свободные места при данном числе занятых."""
        return taken < self.capacity

    def __str__(self) -> str:
        """Вернуть строковое представление курса."""
        return (
            f"{self.title} — вместимость {self.capacity}, "
            f"начало {self.start_date}"
        )

    @staticmethod
    def validate_capacity(capacity: int) -> bool:
        """Проверить корректность лимита мест."""
        return capacity > 0

    @classmethod
    def from_data(cls, data: dict) -> "Course":
        """Создать курс из словаря данных (при загрузке из JSON)."""
        return cls(
            data["id"], data["title"], data["capacity"], data["start_date"]
        )

    def to_dict(self) -> dict:
        """Представить курс в виде словаря для сохранения в JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "capacity": self.capacity,
            "start_date": self.start_date,
        }


def find_course_by_id(courses: list[Course], course_id: int) -> Course | None:
    """Найти курс по идентификатору."""
    for course in courses:
        if course.id == course_id:
            return course
    return None


def find_courses(courses: list[Course], query: str) -> list[Course]:
    """Найти курсы, в названии которых встречается подстрока query."""
    query_lower = query.lower()
    return [c for c in courses if query_lower in c.title.lower()]


def add_course(
    courses: list[Course], title: str, capacity: int, start_date: date
) -> Course:
    """Создать курс, добавить его в коллекцию и вернуть объект.

    Вызывает ValueError, если лимит мест некорректен.
    """
    if not Course.validate_capacity(capacity):
        raise ValueError("Лимит мест должен быть положительным числом")
    course_id = max((c.id for c in courses), default=0) + 1
    course = Course(course_id, title, capacity, start_date.isoformat())
    courses.append(course)
    return course


def sort_courses_by_capacity(courses: list[Course]) -> list[Course]:
    """Вернуть курсы, отсортированные по вместимости (по убыванию)."""
    return sorted(courses, key=lambda c: c.capacity, reverse=True)


def taken_seats(applications: list["Application"], course: Course) -> int:
    """Посчитать количество одобренных заявок на курс."""
    return sum(
        1
        for a in applications
        if a.course is course and a.status == "approved"
    )


def is_course_available(
    applications: list["Application"], course: Course
) -> bool:
    """Проверить, есть ли на курсе свободные места."""
    return course.has_free_seats(taken_seats(applications, course))
