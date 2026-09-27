"""Функции для работы с курсами."""

from datetime import date

from storage import load_json, save_json

COURSES_FILE = "courses.json"


def load_courses() -> dict[int, dict]:
    """Загрузить курсы из файла, приведя идентификаторы к int."""
    raw = load_json(COURSES_FILE, default={})
    return {int(course_id): data for course_id, data in raw.items()}


def save_courses(courses: dict[int, dict]) -> None:
    """Сохранить курсы в файл."""
    save_json(COURSES_FILE, courses)


def add_course(
    courses: dict[int, dict], title: str, capacity: int, start_date: date
) -> int:
    """Добавить курс в словарь courses и вернуть его идентификатор."""
    course_id = max(courses.keys(), default=0) + 1
    courses[course_id] = {
        "title": title,
        "capacity": capacity,
        "start_date": start_date.isoformat(),
    }
    return course_id


def find_courses(courses: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти курсы, в названии которых встречается подстрока query."""
    query_lower = query.lower()
    return {
        course_id: data
        for course_id, data in courses.items()
        if query_lower in data["title"].lower()
    }


def taken_seats(applications: list[dict], course_id: int) -> int:
    """Посчитать количество одобренных заявок на курс."""
    return sum(
        1
        for application in applications
        if application["course_id"] == course_id
        and application["status"] == "approved"
    )


def is_course_available(
    courses: dict[int, dict], applications: list[dict], course_id: int
) -> bool:
    """Проверить, есть ли на курсе свободные места."""
    course = courses[course_id]
    return taken_seats(applications, course_id) < course["capacity"]


def filter_available_courses(
    courses: dict[int, dict], applications: list[dict]
) -> dict[int, dict]:
    """Отобрать курсы, на которых ещё есть свободные места."""
    return {
        course_id: data
        for course_id, data in courses.items()
        if is_course_available(courses, applications, course_id)
    }


def sort_courses_by_capacity(
    courses: dict[int, dict]
) -> list[tuple[int, dict]]:
    """Вернуть курсы, отсортированные по вместимости (по убыванию)."""
    return sorted(
        courses.items(), key=lambda item: item[1]["capacity"], reverse=True
    )
