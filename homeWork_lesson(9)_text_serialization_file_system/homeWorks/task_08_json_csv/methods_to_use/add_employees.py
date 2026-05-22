from homeWorks.task_08_json_csv.methods_to_use.work_with_files import (
    save_employee_to_json,
    save_employee_to_csv
)
from homeWorks.task_08_json_csv.methods_to_use.validators import (
    get_validated_date,
    get_validated_full_name
)


def get_employee_data() -> dict | None:
    print("Для отмены добавления введите 0.")

    name = get_validated_full_name("Введите Имя и Фамилию: ")

    if name is None:
        print("Добавление сотрудника отменено.")
        return None

    birthday = get_validated_date(
        "Введите дату рождения (формат ДД.ММ.ГГГГ): "
    )

    if birthday is None:
        print("Добавление сотрудника отменено.")
        return None

    while True:

        try:
            height_input = input("Введите рост (см): ").strip()

            if height_input == '0':
                print("Добавление сотрудника отменено.")
                return None

            weight_input = input("Введите вес (кг): ").strip()

            if weight_input == '0':
                print("Добавление сотрудника отменено.")
                return None

            height = int(height_input)
            weight = float(weight_input)
            break

        except ValueError:
            print("Ошибка: Неверно введены значения!")

    car_input = input("Есть автомобиль? (да/нет): ").strip().lower()

    if car_input == '0':
        print("Добавление сотрудника отменено.")
        return None

    car = car_input in ['да', 'yes', 'y', '1']

    langs_input = input("Введите языки Программирования через запятую: ")

    if langs_input.strip() == '0':
        print("Добавление сотрудника отменено.")
        return None

    languages = [lang.strip() for lang in langs_input.split(",") if lang.strip()]

    new_employees: dict = {
        "name": name,
        "birthday": birthday,
        "height": height,
        "weight": weight,
        "car": car,
        "languages": languages,
    }

    return new_employees


def add_employee_to_json(json_path: str) -> None:
    new_employee = get_employee_data()

    if new_employee is None:
        return

    save_employee_to_json(new_employee, json_path)
    print("Сотрудник добавлен в JSON.")


def add_employee_to_csv(csv_path: str) -> None:
    new_employee = get_employee_data()

    if new_employee is None:
        return

    save_employee_to_csv(new_employee, csv_path)
    print("Сотрудник добавлен в CSV.")
