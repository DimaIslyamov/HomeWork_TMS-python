from exceptions_project.simple_calculator.input_handler import get_number, get_operation
from exceptions_project.simple_calculator.operations import calculate
from exceptions_project.simple_calculator.validator import validate_operation


def process_calculate() -> int | float:
    first_number = get_number("Введите первое число: ")
    second_number = get_number("Введите второе число: ")

    operation = get_operation()
    validate_operation(operation=operation)

    result = calculate(a=first_number,
                       b=second_number,
                       operation=operation)

    return result
