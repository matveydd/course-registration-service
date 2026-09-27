"""Пакет с классами предметной области сервиса регистрации на курсы."""

from .employees import Employee
from .courses import Course
from .applications import Application
from .results import Result

__all__ = ["Employee", "Course", "Application", "Result"]
