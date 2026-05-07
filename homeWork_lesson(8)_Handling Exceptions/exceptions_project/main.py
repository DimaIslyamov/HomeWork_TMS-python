from bmi.input_handler import get_height, get_weight
from bmi.categories import get_bmi_category
from bmi.calculator import calculate_bmi
from bmi.validator import validate_height, validate_weight

from simple_calculator.input_handler import get_number, get_operation
from simple_calculator.operations import calculate
from simple_calculator.validator import validate_operation

from utils.exceptions import ValidationError, InvalidInputError


# - тут явно можно убрать операции после try и вынести в отдельный файл (operations/calculate)
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


# - тут тоже можно убрать операции после try и вынести в отдельный файл (operations/calculate)
# в цикл добавить предложение об окончании Y / N
def run_calculator():
    while True:
        try:
            first_number = get_number("Введите первое число: ")
            second_number = get_number("Введите второе число: ")

            operation = get_operation()

            validate_operation(operation)

            result = calculate(
                first_number,
                second_number,
                operation
            )

        except InvalidInputError as e:
            print(f"Ошибка ввода: {e}")

        except ValidationError as e:
            print(f"Ошибка вычисления: {e}")

        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

        else:
            print(f"\nРезультат: {result}")
            break

        finally:
            print("Попытка завершена\n")


def main():
    # run_bmi()
    run_calculator()


if __name__ == "__main__":
    main()
