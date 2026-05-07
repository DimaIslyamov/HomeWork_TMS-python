from exceptions_project.simple_calculator.validator import validate_division

# - Переделать через lambda как на уроке
def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    validate_division(b)
    return a / b


# Убрать длинный if/elif через словарь операций
# Использовать диспетчеризацию через словарь как на уроке Lambda
def calculate(a: float, b: float, operation: str) -> float | None:
    if operation == "+":
        return add(a, b)

    elif operation == "-":
        return subtract(a, b)

    elif operation == "*":
        return multiply(a, b)

    elif operation == "/":
        return divide(a, b)

    return None