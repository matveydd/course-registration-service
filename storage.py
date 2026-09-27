"""Загрузка и сохранение объектов предметной области в формате JSON.

JSON остаётся форматом хранения данных (как в ПР2): при сохранении
объекты преобразуются в обычные структуры (словари/списки), при
загрузке — данные преобразуются обратно в объекты моделей. Связанные
объекты (Course, Employee) хранятся в JSON по идентификатору, а при
загрузке восстанавливаются через поиск в уже загруженной коллекции.
"""

import json
from pathlib import Path

from models.applications import Application, find_application_by_id
from models.courses import Course, find_course_by_id
from models.employees import Employee, find_employee_by_id
from models.results import Result

DATA_DIR = Path(__file__).parent / "data"


def _load_raw(filename: str) -> list:
    """Прочитать список словарей из JSON-файла в каталоге data/."""
    path = DATA_DIR / filename
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, используются пустые данные.")
        return []


def _save_raw(filename: str, data: list) -> None:
    """Сохранить список словарей в JSON-файл в каталоге data/."""
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_employees() -> list[Employee]:
    """Загрузить сотрудников из JSON и создать объекты Employee."""
    return [Employee.from_data(item) for item in _load_raw("employees.json")]


def save_employees(employees: list[Employee]) -> None:
    """Сохранить сотрудников в JSON."""
    _save_raw("employees.json", [e.to_dict() for e in employees])


def load_courses() -> list[Course]:
    """Загрузить курсы из JSON и создать объекты Course."""
    return [Course.from_data(item) for item in _load_raw("courses.json")]


def save_courses(courses: list[Course]) -> None:
    """Сохранить курсы в JSON."""
    _save_raw("courses.json", [c.to_dict() for c in courses])


def load_applications(
    courses: list[Course], employees: list[Employee]
) -> list[Application]:
    """Загрузить заявки из JSON, восстановив связи с Course и Employee.

    Заявка, для которой не найден курс или сотрудник, пропускается —
    это защищает программу от повреждённых или устаревших данных.
    """
    applications = []
    for item in _load_raw("applications.json"):
        course = find_course_by_id(courses, item["course_id"])
        employee = find_employee_by_id(employees, item["employee_id"])
        if course is None or employee is None:
            print(
                f"Заявка id={item['id']} пропущена: "
                f"курс или сотрудник не найден."
            )
            continue
        applications.append(
            Application(
                application_id=item["id"],
                employee=employee,
                course=course,
                status=item["status"],
                rejection_reason=item["rejection_reason"],
                history=item["history"],
            )
        )
    return applications


def save_applications(applications: list[Application]) -> None:
    """Сохранить заявки в JSON (по идентификаторам сотрудника и курса)."""
    _save_raw(
        "applications.json",
        [
            {
                "id": a.id,
                "employee_id": a.employee.id,
                "course_id": a.course.id,
                "status": a.status,
                "rejection_reason": a.rejection_reason,
                "history": a.history,
            }
            for a in applications
        ],
    )


def load_results(applications: list[Application]) -> list[Result]:
    """Загрузить результаты из JSON, восстановив связь с Application."""
    results = []
    for item in _load_raw("results.json"):
        application = find_application_by_id(
            applications, item["application_id"]
        )
        if application is None:
            print(
                f"Результат для заявки id={item['application_id']} пропущен."
            )
            continue
        results.append(
            Result(application, item["score"], item["completed_at"])
        )
    return results


def save_results(results: list[Result]) -> None:
    """Сохранить результаты в JSON (по идентификатору заявки)."""
    _save_raw(
        "results.json",
        [
            {
                "application_id": r.application.id,
                "score": r.score,
                "completed_at": r.completed_at,
            }
            for r in results
        ],
    )
