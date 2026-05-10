from exceptions_project.simple_calculator.constants import Operation
from exceptions_project.utils.exceptions import ValidationError


OPERATORS = {
    Operation.ADDITION.value: lambda a, b: a + b,
    Operation.SUBTRACTION.value: lambda a, b: a - b,
    Operation.MULTIPLICATION.value: lambda a, b: a * b,
    Operation.DIVISION.value: lambda a, b: a / b,
}


def calculate(a: float, b: float, operation: str) -> float:
    if operation not in OPERATORS:
        raise ValidationError("Недопустимая операция")

    if operation == Operation.DIVISION.value and b == 0:
        raise ValidationError("На ноль делить нельзя")

    return OPERATORS[operation](a, b)
