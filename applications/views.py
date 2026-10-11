"""Страницы заявок: список и карточка отдельной заявки."""

from django.http import HttpResponse
from django.utils.html import escape

import storage
from homepage.views import page
from models.applications import (
    find_application_by_id,
    get_application_status,
)
from models.results import find_result_for_application

# статус заявки -> (подпись, класс Bootstrap-бейджа)
STATUS_BADGES = {
    "pending": ("на рассмотрении", "bg-warning text-dark"),
    "approved": ("одобрена", "bg-success"),
    "rejected": ("отклонена", "bg-danger"),
    "cancelled": ("отменена", "bg-secondary"),
}


def _load_applications():
    """Загрузить заявки и результаты из JSON-хранилища ПР3."""
    courses_list = storage.load_courses()
    employees = storage.load_employees()
    applications = storage.load_applications(courses_list, employees)
    return applications, storage.load_results(applications)


def _badge(status):
    """Вернуть HTML бейджа для статуса заявки."""
    label, css_class = STATUS_BADGES.get(status, (status, "bg-secondary"))
    return f'<span class="badge {css_class}">{escape(label)}</span>'


def applications(request):
    """Страница /applications/: список заявок со статусами."""
    applications_list, _ = _load_applications()
    items = ""
    for application in applications_list:
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/applications/{application.id}/">
                {escape(application.course.title)} –
                {escape(application.employee.full_name)}
            </a>
            {_badge(application.status)}
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Заявок пока нет.</li>'
    content = f"""
    <h1>Заявки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Заявки", content))


def application_detail(request, application_id):
    """Страница /applications/<id>/; если заявка не найдена – код 404."""
    applications_list, results = _load_applications()
    application = find_application_by_id(applications_list, application_id)

    if application is None:
        content = """
        <h1 class="text-danger">Заявка не найдена</h1>
        <a href="/applications/" class="btn btn-outline-secondary">
            ← к списку заявок
        </a>
        """
        return HttpResponse(page("Заявка не найдена", content), status=404)

    result = find_result_for_application(results, application.id)
    result_html = (
        f"<strong>Результат:</strong> {escape(str(result))}"
        if result
        else "Результат пока не зафиксирован"
    )
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Заявка №{application.id}</h5>
            <p class="card-text">
                <strong>Курс:</strong>
                <a href="/courses/{application.course.id}/">
                    {escape(application.course.title)}
                </a>
            </p>
            <p class="card-text">
                <strong>Сотрудник:</strong>
                {escape(application.employee.full_name)}
                ({escape(application.employee.email)})
            </p>
            <p class="card-text">
                Статус: {_badge(application.status)}
                {escape(get_application_status(application))}
            </p>
            <p class="card-text">{result_html}</p>
            <a href="/applications/" class="btn btn-outline-secondary">
                ← к списку заявок
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Заявка №{application.id}", content), status=200
    )
