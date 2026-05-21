import os

from homeWorks.task_08_json_csv.methods_to_use.add_employees import add_employee_date
from homeWorks.task_08_json_csv.methods_to_use.search_employees import find_employee_by_name
from homeWorks.task_08_json_csv.methods_to_use.filters import filter_by_language, average_height_by_year


current_directory = os.path.dirname(__file__)
data_directory = os.path.join(current_directory, "data")

employees_json_path = os.path.join(data_directory, 'employees.json')
employees_csv_path = os.path.join(data_directory, 'employees.csv')


def main():
    # add_employee_date(json_path=employees_json_path,
    #                   csv_path=employees_csv_path)
    # find_employee_by_name(employees_json_path)
    # filter_by_language(employees_json_path)
    pass


if __name__ == "__main__":
    main()