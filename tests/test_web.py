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


def test_course_list_shows_free_seats(client):
    html = client.get("/courses/").content.decode()
    assert "Основы Python" in html
    assert "свободно 0 из 1" in html


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
