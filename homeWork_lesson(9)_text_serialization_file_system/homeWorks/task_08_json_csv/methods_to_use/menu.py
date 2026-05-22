from homeWorks.task_08_json_csv.methods_to_use.search_employees import find_employee_by_name
from homeWorks.task_08_json_csv.methods_to_use.work_with_files import update_json_to_csv
from homeWorks.task_08_json_csv.methods_to_use.filters import (
    filter_by_language,
    average_height_by_year
)
from homeWorks.task_08_json_csv.methods_to_use.add_employees import (
    add_employee_to_csv,
    add_employee_to_json
)


MENU_TEXT = """
Меню:
1. Преобразовать JSON в CSV и сохранить
2. Добавить сотрудника в JSON
3. Добавить сотрудника в CSV
4. Найти сотрудника по имени
5. Найти сотрудников по языку
6. Средний рост по году рождения
0. Выход
"""


def run_menu(json_path: str, csv_path: str) -> None:
    actions = {
        '1': lambda: update_json_to_csv(json_path, csv_path),
        '2': lambda: add_employee_to_json(json_path),
        '3': lambda: add_employee_to_csv(csv_path),
        '4': lambda: find_employee_by_name(json_path),
        '5': lambda: filter_by_language(json_path),
        '6': lambda: average_height_by_year(json_path),
    }

    while True:

        print(MENU_TEXT)

        choice = input("Выберите действие: ").strip()

        if choice == '0':
            print("Выход из программы")
            break

        action = actions.get(choice)

        if action is None:
            print("Такого пункта нет")
            continue

        action()
