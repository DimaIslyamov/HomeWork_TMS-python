from exceptions_project.simple_calculator.constants import Operation


OPERATORS = {
    Operation.ADDITION.value: lambda a, b: a + b,
    Operation.SUBTRACTION.value: lambda a, b: a - b,
    Operation.MULTIPLICATION.value: lambda a, b: a * b,
    Operation.DIVISION.value: lambda a, b: a / b,
}


def calculate(a: float, b: float, operation: str) -> float:
    assert operation in OPERATORS

    # OPERATORS[operation] возвращает функцию а (a, b) сразу вызывает ее
    return OPERATORS[operation](a, b)
