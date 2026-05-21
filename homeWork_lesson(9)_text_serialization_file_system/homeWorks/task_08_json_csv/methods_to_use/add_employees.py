from homeWorks.task_08_json_csv.methods_to_use.work_with_files import (
    save_employee_to_json,
    update_json_to_csv
)
from homeWorks.task_08_json_csv.methods_to_use.validators import (
    get_validated_date,
    get_validated_full_name
)


def add_employee_date(json_path: str, csv_path: str) -> None:
    name = get_validated_full_name("Введите Имя и Фамилию: ")
    birthday = get_validated_date(
        "Введите дату рождения (формат ДД.ММ.ГГГГ): "
    )

    while True:

        try:
            height = int(input("Введите рост (см): "))
            weight = float(input("Введите вес (кг): "))
            break

        except ValueError:
            print("Ошибка: Неверно введены значения!")

    car_input = input("Есть автомобиль? (да/нет): ").strip().lower()
    car = car_input in ['да', 'yes', 'y', '1']

    langs_input = input("Введите языки Программирования через запятую: ")
    languages = [lang.strip() for lang in langs_input.split(",") if lang.strip()]

    new_employees: dict = {
        "name": name,
        "birthday": birthday,
        "height": height,
        "weight": weight,
        "car": car,
        "languages": languages,
    }
