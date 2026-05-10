from exceptions_project.utils.exceptions import InvalidInputError


def get_float_input(prompt: str) -> float:
    try:
        value = input(prompt)
        return float(value)

    except ValueError:
        raise InvalidInputError("Ошибка неверного ввода")
