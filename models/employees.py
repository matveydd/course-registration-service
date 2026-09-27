"""Класс Employee и функции для работы с коллекцией сотрудников."""


class Employee:
    """Сотрудник компании."""

    def __init__(self, employee_id: int, full_name: str, email: str) -> None:
        """Создать объект сотрудника."""
        self.id = employee_id
        self.full_name = full_name
        self.email = email

    def __str__(self) -> str:
        """Вернуть строковое представление сотрудника."""
        return f"{self.full_name} ({self.email})"

    @classmethod
    def from_data(cls, data: dict) -> "Employee":
        """Создать сотрудника из словаря данных (при загрузке из JSON)."""
        return cls(data["id"], data["full_name"], data["email"])

    def to_dict(self) -> dict:
        """Представить сотрудника в виде словаря для сохранения в JSON."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
        }


def find_employee_by_id(
    employees: list[Employee], employee_id: int
) -> Employee | None:
    """Найти сотрудника по идентификатору."""
    for employee in employees:
        if employee.id == employee_id:
            return employee
    return None


def find_employee_by_name(
    employees: list[Employee], full_name: str
) -> Employee | None:
    """Найти сотрудника по точному совпадению имени (без учёта регистра)."""
    for employee in employees:
        if employee.full_name.lower() == full_name.lower():
            return employee
    return None


def add_employee(
    employees: list[Employee], full_name: str, email: str
) -> Employee:
    """Создать нового сотрудника, добавить его в коллекцию и вернуть объект."""
    employee_id = max((e.id for e in employees), default=0) + 1
    employee = Employee(employee_id, full_name, email)
    employees.append(employee)
    return employee


def get_or_create_employee(
    employees: list[Employee], full_name: str, email: str
) -> Employee:
    """Найти сотрудника по имени либо создать нового, если его ещё нет."""
    employee = find_employee_by_name(employees, full_name)
    if employee is not None:
        return employee
    return add_employee(employees, full_name, email)
