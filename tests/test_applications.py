from datetime import date

import pytest

from models.applications import (
    approve_application,
    cancel_application,
    create_application,
    reject_application,
)
from models.courses import add_course
from models.employees import add_employee


def _make_course_and_employee(capacity: int = 5):
    courses = []
    course = add_course(
        courses, "Введение в Python", capacity, date(2026, 10, 1)
    )
    employees = []
    employee = add_employee(employees, "Иван Иванов", "ivan@company.local")
    return course, employee


def test_create_application_starts_pending():
    course, employee = _make_course_and_employee()
    applications = []
    application = create_application(applications, employee, course)
    assert application.status == "pending"
    assert application.employee is employee
    assert application.course is course
    assert len(applications) == 1


def test_create_application_fails_without_free_seats():
    course, employee = _make_course_and_employee(capacity=1)
    employees = []
    other_employee = add_employee(
        employees, "Пётр Петров", "petr@company.local"
    )
    applications = []
    first = create_application(applications, other_employee, course)
    first.approve()
    with pytest.raises(ValueError):
        create_application(applications, employee, course)


def test_approve_application_changes_status():
    course, employee = _make_course_and_employee()
    applications = []
    application = create_application(applications, employee, course)
    approve_application(applications, application.id)
    assert application.status == "approved"


def test_reject_application_stores_reason():
    course, employee = _make_course_and_employee()
    applications = []
    application = create_application(applications, employee, course)
    reject_application(applications, application.id, "Не хватает опыта")
    assert application.status == "rejected"
    assert application.rejection_reason == "Не хватает опыта"


def test_create_application_fails_if_already_applied():
    course, employee = _make_course_and_employee()
    applications = []
    create_application(applications, employee, course)
    with pytest.raises(ValueError):
        create_application(applications, employee, course)


def test_cancel_application_keeps_it_in_collection():
    course, employee = _make_course_and_employee()
    applications = []
    application = create_application(applications, employee, course)
    cancel_application(applications, application.id)
    assert application.status == "cancelled"
    assert application in applications


def test_cancelled_application_does_not_block_new_one():
    course, employee = _make_course_and_employee()
    applications = []
    first = create_application(applications, employee, course)
    cancel_application(applications, first.id)
    second = create_application(applications, employee, course)
    assert second.status == "pending"
    assert len(applications) == 2
