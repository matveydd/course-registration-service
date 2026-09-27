from models.employees import (
    add_employee,
    find_employee_by_name,
    get_or_create_employee,
)


def test_add_employee_creates_object_with_attributes():
    employees = []
    employee = add_employee(employees, "Иван Иванов", "ivan@company.local")
    assert employee.id == 1
    assert employee.full_name == "Иван Иванов"
    assert employees == [employee]


def test_employee_str_representation():
    employees = []
    employee = add_employee(employees, "Иван Иванов", "ivan@company.local")
    assert str(employee) == "Иван Иванов (ivan@company.local)"


def test_find_employee_by_name_case_insensitive():
    employees = []
    add_employee(employees, "Иван Иванов", "ivan@company.local")
    found = find_employee_by_name(employees, "иван иванов")
    assert found is not None
    assert found.email == "ivan@company.local"


def test_get_or_create_employee_reuses_existing():
    employees = []
    first = add_employee(employees, "Иван Иванов", "ivan@company.local")
    same = get_or_create_employee(
        employees, "Иван Иванов", "ivan@company.local"
    )
    assert same is first
    assert len(employees) == 1
