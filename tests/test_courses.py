from datetime import date

import pytest

from models.applications import create_application
from models.courses import add_course, find_courses, is_course_available
from models.employees import add_employee


def test_add_course_creates_object_with_attributes():
    courses = []
    course = add_course(courses, "Введение в Python", 20, date(2026, 10, 1))
    assert course.id == 1
    assert course.title == "Введение в Python"
    assert course.capacity == 20
    assert courses == [course]


def test_course_str_representation():
    courses = []
    course = add_course(courses, "Введение в Python", 20, date(2026, 10, 1))
    assert "Введение в Python" in str(course)
    assert "20" in str(course)


def test_find_courses_by_title_substring():
    courses = []
    add_course(courses, "Введение в Python", 20, date(2026, 10, 1))
    add_course(courses, "Основы SQL", 15, date(2026, 11, 1))
    found = find_courses(courses, "python")
    assert len(found) == 1
    assert found[0].title == "Введение в Python"


def test_is_course_available_true_without_applications():
    courses = []
    course = add_course(courses, "Введение в Python", 1, date(2026, 10, 1))
    assert is_course_available([], course)


def test_is_course_available_false_when_full():
    courses = []
    course = add_course(courses, "Введение в Python", 1, date(2026, 10, 1))
    employees = []
    employee = add_employee(employees, "Иван Иванов", "ivan@company.local")
    applications = []
    application = create_application(applications, employee, course)
    application.approve()
    assert not is_course_available(applications, course)


def test_add_course_rejects_non_positive_capacity():
    courses = []
    with pytest.raises(ValueError):
        add_course(courses, "Введение в Python", 0, date(2026, 10, 1))
