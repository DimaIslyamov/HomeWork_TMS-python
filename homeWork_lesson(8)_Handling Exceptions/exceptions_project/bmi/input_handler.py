from exceptions_project.utils import InvalidInputError


def parse_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise InvalidInputError("Введите корректное число")


# - Тут явно можно оптимизировать и сделать одну функцию
# def get_float_input(prompt: str) -> float:

def get_height() -> float:
    user_height_value = input("Введите рост (в метрах): ")
    return parse_float(user_height_value)


def get_weight() -> float:
    user_weight_value = input("Введите вес (в килограммах): ")
    return parse_float(user_weight_value)
