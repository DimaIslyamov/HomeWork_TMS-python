from exceptions_project.utils import InvalidInputError


def parse_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise InvalidInputError("Введите корректное число")


def get_number(prompt: str) -> float:
    value = input(prompt)
    return parse_float(value)


def get_operation() -> str:
    return input("Введите операцию (+, -, *, /): ")
