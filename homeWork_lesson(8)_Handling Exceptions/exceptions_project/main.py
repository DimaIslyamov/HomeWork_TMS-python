from exceptions_project.bmi.process_bmi import process_bmi
from exceptions_project.simple_calculator.process_calculator import process_calculate

from exceptions_project.utils.exceptions import ValidationError, InvalidInputError


def run_bmi():
    try:
        bmi, category = process_bmi()

    except InvalidInputError as error:
        print(f'Ошибка ввода: {error}')

    except ValidationError as error:
        print(f"Ошибка ввода данных: {error}")

    except ValueError as error:
        print(f"Какая-то еще ошибка: {error}")

    else:
        print(f"Ваш ИМТ: {bmi:.2f}")
        print(f"Категория: {category.value}")

    finally:
        print("Всего хорошего, пока =)")


def run_calculator():
    while True:
        try:
            result = process_calculate()

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
