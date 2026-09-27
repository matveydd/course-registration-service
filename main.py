"""Точка входа: консольное меню сервиса регистрации на внутренние курсы."""

from applications import (
    approve_application,
    cancel_application,
    create_application,
    find_applications_by_employee,
    get_application_status,
    load_applications,
    reject_application,
    save_applications,
)
from courses import (
    add_course,
    find_courses,
    load_courses,
    save_courses,
    taken_seats,
)
from employees import get_or_create_employee, load_employees, save_employees
from results import (
    evaluate_result,
    get_result_for_application,
    load_results,
    record_result,
    save_results,
)
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


def show_courses(courses: dict[int, dict], applications: list[dict]) -> None:
    """Вывести список курсов с числом свободных мест."""
    if not courses:
        print("Курсов пока нет.")
        return
    for course_id, data in courses.items():
        free = data["capacity"] - taken_seats(applications, course_id)
        print(
            f"[{course_id}] {data['title']} — свободно {free} из "
            f"{data['capacity']} (начало {data['start_date']})"
        )


def show_applications(
    applications: list[dict], courses: dict[int, dict], results: list[dict]
) -> None:
    """Вывести список заявок с их статусом и результатом, если он есть."""
    if not applications:
        print("Заявок пока нет.")
        return
    for application in applications:
        course = courses.get(application["course_id"])
        course_title = course["title"] if course else "?"
        line = (
            f"[{application['id']}] курс «{course_title}»: "
            f"{get_application_status(application)}"
        )
        result = get_result_for_application(results, application["id"])
        if result:
            line += " — " + evaluate_result(result["score"])
        print(line)


def main() -> None:
    """Точка запуска приложения: цикл меню и вызов функций проекта."""
    courses = load_courses()
    applications = load_applications()
    results = load_results()
    employees = load_employees()

    full_name = input_nonempty("Ваше имя: ")
    email = input_nonempty("Ваш email: ")
    employee_id = get_or_create_employee(employees, full_name, email)
    save_employees(employees)

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
                course_id = add_course(courses, title, capacity, start_date)
                save_courses(courses)
                print(f"Курс создан, идентификатор {course_id}")

            elif choice == "4":
                show_courses(courses, applications)
                course_id = input_int("Идентификатор курса: ")
                application = create_application(
                    courses, applications, employee_id, course_id
                )
                save_applications(applications)
                print(f"Заявка создана, идентификатор {application['id']}")

            elif choice == "5":
                show_applications(applications, courses, results)
                application_id = input_int("Идентификатор заявки: ")
                decision = input_nonempty("1 — одобрить, 2 — отклонить: ")
                if decision == "1":
                    approve_application(courses, applications, application_id)
                    print("Заявка одобрена")
                elif decision == "2":
                    reason = input_nonempty("Причина отклонения: ")
                    reject_application(applications, application_id, reason)
                    print("Заявка отклонена")
                else:
                    print("Нужно ввести 1 или 2.")
                save_applications(applications)

            elif choice == "6":
                show_applications(applications, courses, results)
                application_id = input_int("Идентификатор заявки: ")
                score = input_int("Количество баллов: ")
                completed_at = input_date("Дата завершения (ДД.ММ.ГГГГ): ")
                record_result(
                    applications, results, application_id, score, completed_at
                )
                save_results(results)
                print("Результат зафиксирован")

            elif choice == "7":
                show_applications(
                    find_applications_by_employee(applications, employee_id),
                    courses,
                    results,
                )

            elif choice == "8":
                application_id = input_int("Идентификатор заявки: ")
                cancel_application(applications, application_id)
                save_applications(applications)
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
