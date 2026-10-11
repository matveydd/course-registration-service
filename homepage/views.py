"""Главная страница проекта."""

from django.shortcuts import render


def index(request):
    """Главная страница: описание приложения и ссылки на разделы."""
    return render(request, "homepage/index.html")
