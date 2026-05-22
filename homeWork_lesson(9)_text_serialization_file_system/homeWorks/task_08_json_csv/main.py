import os

from homeWorks.task_08_json_csv.methods_to_use.menu import run_menu

current_directory = os.path.dirname(__file__)
data_directory = os.path.join(current_directory, "data")

employees_json_path = os.path.join(data_directory, 'employees.json')
employees_csv_path = os.path.join(data_directory, 'employees.csv')


def main():
    run_menu(employees_json_path, employees_csv_path)


if __name__ == "__main__":
    main()