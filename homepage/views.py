"""Главная страница и общий HTML-каркас всех страниц проекта."""

from django.http import HttpResponse
from django.utils.html import escape


def page(title, content):
    """Собрать HTML-документ: кодировка, заголовок, Bootstrap, навигация."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav container py-2">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/courses/">Курсы</a>
        <a class="nav-link" href="/applications/">Заявки</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница: описание приложения и ссылки на разделы."""
    content = """
    <h1 class="display-4">Регистрация на курсы</h1>
    <p class="lead">
        Сервис регистрации сотрудников на внутренние курсы компании.
    </p>
    <p>Основные разделы:</p>
    <a href="/courses/" class="btn btn-primary me-2">Курсы</a>
    <a href="/applications/" class="btn btn-secondary">Заявки</a>
    """
    return HttpResponse(page("Регистрация на курсы", content))
