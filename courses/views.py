"""Страницы курсов: список и карточка отдельного курса."""

from django.http import HttpResponse
from django.utils.html import escape

import storage
from homepage.views import page
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
    items = ""
    for course in courses_list:
        free = course.capacity - taken_seats(applications, course)
        items += f"""
        <li class="list-group-item">
            <a href="/courses/{course.id}/">{escape(course.title)}</a>
            – свободно {free} из {course.capacity} мест
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Курсов пока нет.</li>'
    content = f"""
    <h1>Курсы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Курсы", content))


def course_detail(request, course_id):
    """Страница /courses/<id>/; если курс не найден – код статуса 404."""
    courses_list, applications = _load_courses_and_applications()
    course = find_course_by_id(courses_list, course_id)

    if course is None:
        content = """
        <h1 class="text-danger">Курс не найден</h1>
        <a href="/courses/" class="btn btn-outline-secondary">
            ← к списку курсов
        </a>
        """
        return HttpResponse(page("Курс не найден", content), status=404)

    taken = taken_seats(applications, course)
    free = course.capacity - taken
    available = course.has_free_seats(taken)
    status = "есть свободные места" if available else "мест нет"
    badge = "bg-success" if available else "bg-danger"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(course.title)}</h5>
            <p class="card-text"><strong>ID:</strong> {course.id}</p>
            <p class="card-text">
                <strong>Вместимость:</strong> {course.capacity} мест
            </p>
            <p class="card-text">
                <strong>Начало:</strong> {escape(course.start_date)}
            </p>
            <p class="card-text">
                Свободно мест: {free}
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/courses/" class="btn btn-outline-secondary">
                ← к списку курсов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(course.title, content), status=200)
