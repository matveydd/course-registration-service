from datetime import date

employee_name = "Иванова Анна Сергеевна"
employee_email = "a.ivanova@company.local"

course_title = "Введение в аналитику данных"
course_capacity = 20
course_start_date = date(2026, 10, 12)

applications_submitted = 18
result_score_input = "87"


def format_course_info(title, start_date):
    return f"Курс: {title}. Дата начала: {start_date}"


def has_available_seats(capacity, submitted_count):
    return submitted_count < capacity


def get_application_status(has_seats):
    if has_seats:
        return "Заявка принята к рассмотрению"
    else:
        return "Мест нет, заявка отклонена"


def evaluate_result(score_raw):
    score = int(score_raw)
    if score >= 90:
        return f"Результат: {score} баллов — высокий балл"
    elif score >= 50:
        return f"Результат: {score} баллов — средний балл"
    else:
        return f"Результат: {score} баллов — низкий балл"


print(format_course_info(course_title, course_start_date))
print(f"Сотрудник: {employee_name} ({employee_email})")

seats_available = has_available_seats(course_capacity, applications_submitted)
print(f"Свободные места: {course_capacity - applications_submitted}")
print(get_application_status(seats_available))

print(evaluate_result(result_score_input))
