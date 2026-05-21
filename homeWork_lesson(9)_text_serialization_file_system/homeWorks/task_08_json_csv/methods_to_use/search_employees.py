import json


def find_employee_by_name(json_path: str) -> None:
    with open(json_path, 'r', encoding='utf-8') as json_file:
        employees = json.load(json_file)

        user_search_name = input("Введите имя сотрудника: ").strip().lower()

        for employee in employees:

            employee_name = employee['name'].lower()

            if employee_name == user_search_name:

                for key, value in employee.items():

                    if isinstance(value, list):
                        value = ', '.join(value)

                    print(f"{key}: {value}")

                return

        else:

            print("Сотрудник не найден")
