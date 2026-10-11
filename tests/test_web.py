"""Тесты веб-слоя Django: маршруты, коды статуса и содержимое страниц."""

import json
import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coursereg.settings")
django.setup()

import storage  # noqa: E402
from django.test import Client  # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from django.urls import reverse  # noqa: E402

setup_test_environment()


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Клиент Django с изолированным каталогом данных."""
    data = {
        "courses.json": [
            {"id": 1, "title": "Основы Python", "capacity": 1,
             "start_date": "2026-11-03"},
        ],
        "employees.json": [
            {"id": 1, "full_name": "Иванов Иван", "email": "i@example.com"},
        ],
        "applications.json": [
            {"id": 1, "employee_id": 1, "course_id": 1,
             "status": "approved", "rejection_reason": None,
             "history": [{"from": None, "to": "pending"}]},
        ],
        "results.json": [
            {"application_id": 1, "score": 95, "completed_at": "2026-11-10"},
        ],
    }
    for name, content in data.items():
        (tmp_path / name).write_text(
            json.dumps(content, ensure_ascii=False), encoding="utf-8"
        )
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    return Client()


@pytest.mark.parametrize(
    "url", ["/", "/courses/", "/courses/1/", "/applications/",
            "/applications/1/"]
)
def test_pages_return_200(client, url):
    assert client.get(url).status_code == 200


def test_course_list_shows_free_seats_and_count(client):
    html = client.get("/courses/").content.decode()
    assert "Основы Python" in html
    assert "Свободно мест: 0 из 1" in html
    assert "Всего курсов: 1" in html


def test_course_detail_shows_no_seats_badge(client):
    html = client.get("/courses/1/").content.decode()
    assert "мест нет" in html
    assert "bg-danger" in html


def test_application_detail_shows_related_objects_and_result(client):
    html = client.get("/applications/1/").content.decode()
    assert "Основы Python" in html
    assert "Иванов Иван" in html
    assert "95 баллов" in html


@pytest.mark.parametrize("url", ["/courses/999/", "/applications/999/"])
def test_unknown_id_returns_404(client, url):
    assert client.get(url).status_code == 404


def test_pages_include_bootstrap_and_navigation(client):
    html = client.get("/").content.decode()
    assert "bootstrap@5.3.3" in html
    assert 'href="/courses/"' in html
    assert 'href="/applications/"' in html


@pytest.mark.parametrize(
    "url, template",
    [
        ("/", "homepage/index.html"),
        ("/courses/", "courses/course_list.html"),
        ("/courses/1/", "courses/course_detail.html"),
        ("/applications/", "applications/application_list.html"),
        ("/applications/1/", "applications/application_detail.html"),
    ],
)
def test_pages_use_templates_with_base(client, url, template):
    response = client.get(url)
    names = [t.name for t in response.templates]
    assert template in names
    assert "base.html" in names
    assert "includes/navigation.html" in names


def test_includes_are_used(client):
    names = [t.name for t in client.get("/courses/").templates]
    assert "courses/includes/course_card.html" in names
    names = [t.name for t in client.get("/applications/").templates]
    assert "applications/includes/application_status.html" in names


def test_named_urls_are_resolved(client):
    assert reverse("homepage:index") == "/"
    assert reverse("courses:list") == "/courses/"
    assert reverse("courses:detail", args=[1]) == "/courses/1/"
    assert reverse("applications:list") == "/applications/"
    assert reverse("applications:detail", args=[1]) == "/applications/1/"


def test_links_are_built_from_named_urls(client):
    html = client.get("/courses/").content.decode()
    assert 'href="/courses/1/"' in html


def test_static_files_are_linked_in_base_template(client):
    html = client.get("/").content.decode()
    assert "/static/homepage/css/style.css" in html
    assert "/static/homepage/img/logo.png" in html
    assert "/static/homepage/js/main.js" in html


def test_404_pages_show_messages(client):
    html = client.get("/courses/999/").content.decode()
    assert "Курс не найден" in html
    html = client.get("/applications/999/").content.decode()
    assert "Заявка не найдена" in html


def test_empty_collections_show_empty_messages(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    client = Client()
    assert "Курсы не найдены." in client.get("/courses/").content.decode()
    html = client.get("/applications/").content.decode()
    assert "Заявки не найдены." in html


def test_application_status_variants(client):
    html = client.get("/applications/").content.decode()
    assert "application-status-approved" in html


def test_page_helper_is_removed():
    import homepage.views

    assert not hasattr(homepage.views, "page")
