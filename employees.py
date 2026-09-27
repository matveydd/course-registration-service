"""Функции для работы с сотрудниками."""

from storage import load_json, save_json

EMPLOYEES_FILE = "employees.json"


def load_employees() -> dict[int, dict]:
    """Загрузить сотрудников из файла, приведя идентификаторы к int."""
    raw = load_json(EMPLOYEES_FILE, default={})
    return {int(employee_id): data for employee_id, data in raw.items()}


def save_employees(employees: dict[int, dict]) -> None:
    """Сохранить сотрудников в файл."""
    save_json(EMPLOYEES_FILE, employees)


def find_employee_by_name(
    employees: dict[int, dict], full_name: str
) -> int | None:
    """Найти сотрудника по точному совпадению имени (без учёта регистра)."""
    for employee_id, data in employees.items():
        if data["full_name"].lower() == full_name.lower():
            return employee_id
    return None


def add_employee(
    employees: dict[int, dict], full_name: str, email: str
) -> int:
    """Добавить нового сотрудника и вернуть его идентификатор."""
    employee_id = max(employees.keys(), default=0) + 1
    employees[employee_id] = {"full_name": full_name, "email": email}
    return employee_id


def get_or_create_employee(
    employees: dict[int, dict], full_name: str, email: str
) -> int:
    """Найти сотрудника по имени либо создать нового, если его ещё нет."""
    employee_id = find_employee_by_name(employees, full_name)
    if employee_id is not None:
        return employee_id
    return add_employee(employees, full_name, email)
