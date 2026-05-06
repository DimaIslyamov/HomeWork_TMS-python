from bmi.input_handler import get_height, get_weight
from bmi.categories import get_bmi_category
from bmi.calculator import calculate_bmi
from bmi.validator import validate_height, validate_weight

from utils.exceptions import ValidationError, InvalidInputError


def run_bmi():
    try:
        height = get_height()
        weight = get_weight()

        validate_height(height)
        validate_weight(weight)

        bmi = calculate_bmi(height, weight)
        category = get_bmi_category(bmi)

    except InvalidInputError as error:
        print(f'Ошибка ввода: {error}')

    except ValidationError as error:
        print(f"Ошибка ввода данных: {error}")

    except ValueError as error:
        print(f"Какая-то еще ошибка: {error}")

    else:
        print(f"Ваш ИМТ: {bmi:.2f}")
        print(f"Категория: {category:.2f}")

    finally:
        print("Всего хорошего, пока =)")


def main():
    run_bmi()


if __name__ == "__main__":
    main()