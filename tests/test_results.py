from datetime import date

import pytest

from models.applications import create_application
from models.courses import add_course
from models.employees import add_employee
from models.results import record_result


def _make_approved_application():
    courses = []
    course = add_course(courses, "Введение в Python", 5, date(2026, 10, 1))
    employees = []
    employee = add_employee(employees, "Иван Иванов", "ivan@company.local")
    applications = []
    application = create_application(applications, employee, course)
    application.approve()
    return applications, application


def test_record_result_for_approved_application():
    applications, application = _make_approved_application()
    results = []
    result = record_result(
        applications, results, application.id, 95, date(2026, 10, 20)
    )
    assert result.score == 95
    assert result.application is application
    assert results == [result]


def test_record_result_fails_for_pending_application():
    courses = []
    course = add_course(courses, "Введение в Python", 5, date(2026, 10, 1))
    employees = []
    employee = add_employee(employees, "Иван Иванов", "ivan@company.local")
    applications = []
    application = create_application(applications, employee, course)
    with pytest.raises(ValueError):
        record_result(applications, [], application.id, 95, date(2026, 10, 20))


def test_record_result_twice_fails():
    applications, application = _make_approved_application()
    results = []
    record_result(
        applications, results, application.id, 95, date(2026, 10, 20)
    )
    with pytest.raises(ValueError):
        record_result(
            applications, results, application.id, 80, date(2026, 10, 21)
        )


def test_evaluate_score_levels():
    applications, application = _make_approved_application()
    results = []
    high = record_result(
        applications, results, application.id, 95, date(2026, 10, 20)
    )
    assert high.evaluate() == "высокий балл"
