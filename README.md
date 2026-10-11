# Сервис регистрации сотрудников на внутренние курсы

Консольное приложение для подачи заявок на внутренние курсы компании, их
рассмотрения и фиксации результатов обучения.

## Возможности
- создание курсов;
- просмотр и поиск курсов по названию;
- подача заявки на курс с проверкой свободных мест;
- рассмотрение заявки (одобрение или отклонение с указанием причины);
- отмена заявки (без удаления — сохраняется в истории со статусом «cancelled»);
- фиксация результата прохождения курса (баллы);
- просмотр своих заявок и результатов;
- просмотр курсов и заявок в браузере (веб-интерфейс на Django,
  страницы формируются шаблонами).

## Используемые технологии
- Python 3.14;
- Django 5.2 — веб-фреймворк;
- Django Template Language (DTL) — шаблоны страниц;
- HTML5 — разметка веб-страниц;
- CSS3, собственный `style.css` и Bootstrap 5.3 — оформление страниц;
- JavaScript — небольшое клиентское поведение (`main.js`);
- JSON — хранение данных;
- pytest — автоматизированные тесты;
- flake8 — проверка качества кода.

## Основные классы

### `Employee` (`models/employees.py`)
Сотрудник компании.
- Атрибуты: `id`, `full_name`, `email`.
- Методы: `__str__()` — строковое представление; `from_data()` /
  `to_dict()` — преобразование в/из JSON.

### `Course` (`models/courses.py`)
Курс, доступный для подачи заявок.
- Атрибуты: `id`, `title`, `capacity`, `start_date`.
- Методы: `has_free_seats(taken)` — проверка наличия мест;
  `validate_capacity(capacity)` (`@staticmethod`) — корректность лимита;
  `__str__()`; `from_data()` / `to_dict()`.

### `Application` (`models/applications.py`)
Заявка сотрудника на курс. Хранит ссылки на объекты `Employee` и
`Course` (а не их идентификаторы).
- Атрибуты: `id`, `employee`, `course`, `status`, `rejection_reason`,
  `history` (список переходов статуса).
- Методы: `approve()`, `reject(reason)`, `cancel()` — меняют состояние
  объекта, не удаляя его из коллекции; `__str__()`.

### `Result` (`models/results.py`)
Результат прохождения курса. Хранит ссылку на объект `Application`.
- Атрибуты: `application`, `score`, `completed_at`.
- Методы: `evaluate()` — текстовая оценка по баллам; `__str__()`.

## Взаимодействие объектов

```
Employee ──создаёт──> Application <──относится к── Course
                           │
                           └──результат──> Result
```

`Application` не хранит `employee_id`/`course_id` — она напрямую ссылается
на объекты `Employee` и `Course`, поэтому `application.employee.full_name`
и `application.course.title` доступны без дополнительного поиска.
В JSON, наоборот, сохраняются только идентификаторы — связи
восстанавливаются функциями `storage.py` при загрузке.

## Структура проекта
```
course_registration/
├── manage.py                — управление Django-проектом
├── main.py                  — консольная версия (сохранена с ПР3)
├── storage.py               — загрузка/сохранение объектов в JSON
├── utils.py                 — безопасный ввод
├── requirements.txt
├── coursereg/               — конфигурация Django-проекта
│   ├── settings.py
│   └── urls.py              — маршрутизация верхнего уровня
├── templates/               — шаблоны уровня проекта
│   ├── base.html            — базовый шаблон
│   └── includes/
│       └── navigation.html  — навигация
├── homepage/
│   ├── templates/homepage/index.html
│   ├── static/homepage/
│   │   ├── css/style.css    — собственный CSS
│   │   ├── js/main.js       — собственный JavaScript
│   │   └── img/logo.png     — логотип
│   ├── views.py
│   └── urls.py
├── courses/
│   ├── templates/courses/
│   │   ├── course_list.html
│   │   ├── course_detail.html
│   │   └── includes/course_card.html
│   ├── views.py
│   └── urls.py
├── applications/
│   ├── templates/applications/
│   │   ├── application_list.html
│   │   ├── application_detail.html
│   │   └── includes/application_status.html
│   ├── views.py
│   └── urls.py
├── models/                  — классы предметной области (ПР3)
│   ├── employees.py         — Employee
│   ├── courses.py           — Course
│   ├── applications.py      — Application
│   └── results.py           — Result
├── data/                    — JSON-файлы данных
└── tests/                   — автоматизированные тесты
```

Файлы `models.py` Django-приложений пока пустые: пакет `models/` с
классами предметной области (ПР3) продолжает использоваться как источник
данных для веб-интерфейса. Django ORM и база данных не используются.

## Веб-интерфейс (Django)

Веб-часть реализована на Django. Основные страницы:
- главная страница;
- список курсов;
- информация об отдельном курсе;
- список заявок;
- информация об отдельной заявке.

Для формирования страниц используются Django-шаблоны. HTML в
Python-коде веб-представлений не формируется, функция `page()` из ПР5
удалена. Представления загружают данные средствами ПР3, подготавливают
контекст и вызывают `render()`.

| URL                                   | Имя маршрута            | Шаблон                                    |
|---------------------------------------|-------------------------|-------------------------------------------|
| `/`                                   | `homepage:index`        | `homepage/index.html`                     |
| `/courses/`                           | `courses:list`          | `courses/course_list.html`                |
| `/courses/<int:course_id>/`           | `courses:detail`        | `courses/course_detail.html`              |
| `/applications/`                      | `applications:list`     | `applications/application_list.html`      |
| `/applications/<int:application_id>/` | `applications:detail`   | `applications/application_detail.html`    |

Если курс или заявка не найдены, шаблон выводит сообщение, а ответ
имеет код статуса 404 (`status=404 if obj is None else 200`).

## Django Template Language

### Базовый шаблон и наследование
Общая структура страниц находится в `templates/base.html`: кодировка,
`{% block title %}`, подключение Bootstrap и собственных статических
файлов, логотип, навигация, `{% block content %}`, подвал. Дочерние
шаблоны используют `{% extends "base.html" %}` и переопределяют блоки.
Каталог `templates/` подключён в `TEMPLATES["DIRS"]`.

### Включаемые шаблоны
- `templates/includes/navigation.html` — навигация сайта;
- `courses/includes/course_card.html` — карточка курса;
- `applications/includes/application_status.html` — статус заявки
  (используется в списке и на странице заявки).

Подключение: `{% include "courses/includes/course_card.html" %}`.

### Контекст
Представления передают данные словарём `context`, например для списка
курсов `{"items": items}`; в шаблоне `{% for item in items %}`.

### Циклы и условия
`{% for %}` с `{% empty %}` (сообщения «Курсы не найдены.»,
«Заявки не найдены.»); `{% if %}` / `{% elif %}` / `{% else %}` для
статуса заявки, наличия мест и отсутствующего объекта.

### Именованные URL и пространства имён
В `urls.py` каждого приложения задан `app_name` (`homepage`, `courses`,
`applications`). Ссылки строятся тегом `{% url %}`:
`{% url 'courses:detail' course.id %}`, `{% url 'applications:list' %}`.

### Фильтры
`{{ items|length }}` и `{{ applications|length }}` — количество
элементов; `{{ course.title|default:"Без названия" }}` — значение по
умолчанию. Дата начала курса хранится как строка и выводится без
преобразования.

### Статические файлы
`homepage/static/homepage/`: `css/style.css`, `js/main.js`,
`img/logo.png`. В шаблонах: `{% load static %}` и
`{% static 'homepage/css/style.css' %}`. `main.js` выводит текущий год в
подвале; собственные стили оформляют логотип, карточки курсов и статусы
заявок. Проверка: `python manage.py findstatic homepage/img/logo.png`.

## Формат данных
Данные хранятся в каталоге `data/` в формате JSON (списки объектов):
- `courses.json`, `employees.json` — список курсов/сотрудников;
- `applications.json` — заявки по `employee_id`/`course_id`;
- `results.json` — результаты по `application_id`.

При загрузке JSON преобразуется в объекты классов; при сохранении —
обратно в словари. Функция `record_result()`, методы `approve()` /
`reject()` / `cancel()` продолжают опираться на обработку исключений
(`ValueError`) для всех нарушений бизнес-правил, как и в ПР2.

## Требования
- Python 3.14;
- Django 5.2.*;
- pytest;
- flake8.

Установка зависимостей:
```
pip install -r requirements.txt
```

## Запуск программы
Веб-версия (Django):
```
python manage.py migrate
python manage.py runserver
```
После запуска открыть в браузере http://127.0.0.1:8000/

Консольная версия (сохранена):
```
python main.py
```

## Запуск тестов
```
pytest -v
```
Тесты консольной части (ПР3) и тесты веб-слоя (`tests/test_web.py`):
коды ответов, используемые шаблоны, именованные URL, статические файлы,
страницы 404, пустые коллекции.

Проверка проекта Django:
```
python manage.py check
```

## Проверка качества кода
```
flake8 . --extend-exclude=venv
```

## Текущее состояние и план развития
Реализовано: консольная версия на объектной модели (ПР3); Django-проект,
маршрутизация, view-функции (ПР5); шаблоны Django, базовый шаблон,
включаемые шаблоны, фильтры, именованные URL, статические файлы,
собственные CSS и JavaScript (ПР6).

Пока не реализовано: данные хранятся в JSON, Django ORM не
используется, формы Django отсутствуют; работа с базой данных относится
к следующим практическим работам.

На следующих этапах планируется:
- перенос сущностей в Django ORM, подключение базы данных;
- формы создания курсов и заявок;
- реализация пользователей и ролей (сотрудник/куратор);
- разработка API;
- контейнеризация приложения;
- настройка CI/CD.
