"""Страницы заявок: список и карточка отдельной заявки."""

from django.shortcuts import render

import storage
from models.applications import (
    find_application_by_id,
    get_application_status,
)
from models.results import find_result_for_application


def _load_applications():
    """Загрузить заявки и результаты из JSON-хранилища ПР3."""
    courses_list = storage.load_courses()
    employees = storage.load_employees()
    applications = storage.load_applications(courses_list, employees)
    return applications, storage.load_results(applications)


def applications(request):
    """Страница /applications/: список заявок со статусами."""
    applications_list, _ = _load_applications()

    context = {
        "applications": applications_list,
    }

    return render(request, "applications/application_list.html", context)


def application_detail(request, application_id):
    """Страница /applications/<id>/; если заявка не найдена – код 404."""
    applications_list, results = _load_applications()
    application = find_application_by_id(applications_list, application_id)

    context = {"application": application}
    if application is not None:
        context["result"] = find_result_for_application(
            results, application.id
        )
        context["status_text"] = get_application_status(application)

    return render(
        request,
        "applications/application_detail.html",
        context,
        status=404 if application is None else 200,
    )
