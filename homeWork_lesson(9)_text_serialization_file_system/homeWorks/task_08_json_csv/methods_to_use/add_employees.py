import os

from homeWorks.task_08_json_csv.methods_to_use.validate_date import get_validated_date


def add_employees_date(json_path: str, csv_path: str) -> None:
    name = input("Введите Имя и Фамилию: ").strip()
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

# //// дописать -- 