"""Точка входа: консольное меню сервиса регистрации на внутренние курсы."""

import storage
from models.applications import (
    Application,
    approve_application,
    cancel_application,
    create_application,
    find_applications_by_employee,
    get_application_status,
    reject_application,
)
from models.courses import (
    Course,
    add_course,
    find_course_by_id,
    find_courses,
    taken_seats,
)
from models.employees import get_or_create_employee
from models.results import Result, find_result_for_application, record_result
from utils import input_date, input_int, input_nonempty

MENU = """
=== Сервис регистрации на внутренние курсы ===
1. Показать курсы
2. Найти курс по названию
3. Создать курс
4. Подать заявку на курс
5. Рассмотреть заявку (одобрить/отклонить)
6. Зафиксировать результат
7. Показать мои заявки
8. Отменить заявку
0. Выход
"""


def show_courses(
    courses: list[Course], applications: list[Application]
) -> None:
    """Вывести список курсов с числом свободных мест."""
    if not courses:
        print("Курсов пока нет.")
        return
    for course in courses:
        free = course.capacity - taken_seats(applications, course)
        print(
            f"[{course.id}] {course.title} — свободно {free} из "
            f"{course.capacity} (начало {course.start_date})"
        )


def show_applications(
    applications: list[Application], results: list[Result]
) -> None:
    """Вывести список заявок с их статусом и результатом, если он есть."""
    if not applications:
        print("Заявок пока нет.")
        return
    for application in applications:
        line = (
            f"[{application.id}] курс «{application.course.title}»: "
            f"{get_application_status(application)}"
        )
        result = find_result_for_application(results, application.id)
        if result:
            line += " — " + str(result)
        print(line)


def main() -> None:
    """Точка запуска приложения: цикл меню и вызов функций проекта."""
    courses = storage.load_courses()
    employees = storage.load_employees()
    applications = storage.load_applications(courses, employees)
    results = storage.load_results(applications)

    full_name = input_nonempty("Ваше имя: ")
    email = input_nonempty("Ваш email: ")
    employee = get_or_create_employee(employees, full_name, email)
    storage.save_employees(employees)

    while True:
        print(MENU)
        choice = input_nonempty("Выберите действие: ")

        try:
            if choice == "1":
                show_courses(courses, applications)

            elif choice == "2":
                query = input_nonempty("Подстрока названия: ")
                show_courses(find_courses(courses, query), applications)

            elif choice == "3":
                title = input_nonempty("Название курса: ")
                capacity = input_int("Лимит мест: ")
                start_date = input_date("Дата начала (ДД.ММ.ГГГГ): ")
                course = add_course(courses, title, capacity, start_date)
                storage.save_courses(courses)
                print(f"Курс создан, идентификатор {course.id}")

            elif choice == "4":
                show_courses(courses, applications)
                course_id = input_int("Идентификатор курса: ")
                course = find_course_by_id(courses, course_id)
                if course is None:
                    raise ValueError("Курс с таким идентификатором не найден")
                application = create_application(
                    applications, employee, course
                )
                storage.save_applications(applications)
                print(f"Заявка создана, идентификатор {application.id}")

            elif choice == "5":
                show_applications(applications, results)
                application_id = input_int("Идентификатор заявки: ")
                decision = input_nonempty("1 — одобрить, 2 — отклонить: ")
                if decision == "1":
                    approve_application(applications, application_id)
                    print("Заявка одобрена")
                elif decision == "2":
                    reason = input_nonempty("Причина отклонения: ")
                    reject_application(applications, application_id, reason)
                    print("Заявка отклонена")
                else:
                    print("Нужно ввести 1 или 2.")
                storage.save_applications(applications)

            elif choice == "6":
                show_applications(applications, results)
                application_id = input_int("Идентификатор заявки: ")
                score = input_int("Количество баллов: ")
                completed_at = input_date("Дата завершения (ДД.ММ.ГГГГ): ")
                record_result(
                    applications, results, application_id, score, completed_at
                )
                storage.save_results(results)
                print("Результат зафиксирован")

            elif choice == "7":
                my_applications = find_applications_by_employee(
                    applications, employee
                )
                show_applications(my_applications, results)

            elif choice == "8":
                application_id = input_int("Идентификатор заявки: ")
                cancel_application(applications, application_id)
                storage.save_applications(applications)
                print("Заявка отменена")

            elif choice == "0":
                print("До встречи!")
                break

            else:
                print("Такого пункта меню нет, попробуйте ещё раз.")

        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
