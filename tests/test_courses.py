from datetime import date

from courses import add_course, find_courses, is_course_available


def test_add_course():
    courses = {}
    course_id = add_course(courses, "Введение в Python", 20, date(2026, 10, 1))
    assert course_id == 1
    assert courses[1]["title"] == "Введение в Python"


def test_find_courses():
    courses = {}
    add_course(courses, "Введение в Python", 20, date(2026, 10, 1))
    add_course(courses, "Основы SQL", 15, date(2026, 11, 1))
    found = find_courses(courses, "python")
    assert len(found) == 1


def test_is_course_available_true_without_applications():
    courses = {}
    course_id = add_course(courses, "Введение в Python", 1, date(2026, 10, 1))
    assert is_course_available(courses, [], course_id)


def test_is_course_available_false_when_full():
    courses = {}
    course_id = add_course(courses, "Введение в Python", 1, date(2026, 10, 1))
    applications = [{"course_id": course_id, "status": "approved"}]
    assert not is_course_available(courses, applications, course_id)
