"""Страницы курсов: список и карточка отдельного курса."""

from django.shortcuts import render

import storage
from models.courses import find_course_by_id, taken_seats


def _load_courses_and_applications():
    """Загрузить курсы и заявки из JSON-хранилища ПР3."""
    courses_list = storage.load_courses()
    employees = storage.load_employees()
    applications = storage.load_applications(courses_list, employees)
    return courses_list, applications


def courses(request):
    """Страница /courses/: список курсов с числом свободных мест."""
    courses_list, applications = _load_courses_and_applications()

    items = [
        {
            "course": course,
            "free": course.capacity - taken_seats(applications, course),
        }
        for course in courses_list
    ]
    context = {
        "items": items,
    }

    return render(request, "courses/course_list.html", context)


def course_detail(request, course_id):
    """Страница /courses/<id>/; если курс не найден – код статуса 404."""
    courses_list, applications = _load_courses_and_applications()
    course = find_course_by_id(courses_list, course_id)

    context = {"course": course}
    if course is not None:
        taken = taken_seats(applications, course)
        context["free"] = course.capacity - taken
        context["available"] = course.has_free_seats(taken)

    return render(
        request,
        "courses/course_detail.html",
        context,
        status=404 if course is None else 200,
    )
