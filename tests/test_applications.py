from datetime import date

import pytest

from applications import (
    approve_application,
    create_application,
    reject_application,
)
from courses import add_course


def test_create_application():
    courses = {}
    course_id = add_course(courses, "Введение в Python", 5, date(2026, 10, 1))
    applications = []
    application = create_application(
        courses, applications, employee_id=1, course_id=course_id
    )
    assert application["status"] == "pending"
    assert len(applications) == 1


def test_create_application_fails_without_free_seats():
    courses = {}
    course_id = add_course(courses, "Введение в Python", 1, date(2026, 10, 1))
    applications = [
        {
            "id": 1,
            "employee_id": 2,
            "course_id": course_id,
            "status": "approved",
        }
    ]
    with pytest.raises(ValueError):
        create_application(
            courses, applications, employee_id=1, course_id=course_id
        )


def test_approve_application():
    courses = {}
    course_id = add_course(courses, "Введение в Python", 5, date(2026, 10, 1))
    applications = []
    application = create_application(
        courses, applications, employee_id=1, course_id=course_id
    )
    approve_application(courses, applications, application["id"])
    assert application["status"] == "approved"


def test_reject_application_stores_reason():
    courses = {}
    course_id = add_course(courses, "Введение в Python", 5, date(2026, 10, 1))
    applications = []
    application = create_application(
        courses, applications, employee_id=1, course_id=course_id
    )
    reject_application(applications, application["id"], "Не хватает опыта")
    assert application["status"] == "rejected"
    assert application["rejection_reason"] == "Не хватает опыта"
