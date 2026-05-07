from exceptions_project.utils import InvalidInputError

# - Тут можно Объединить ввод чисел | def get_two_numbers():

def parse_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise InvalidInputError("Введите корректное число")


def get_number(prompt: str) -> float:
    value = input(prompt)
    return parse_float(value)


def get_operation() -> str:
    return input("Выберите операцию (+, -, *, /): ")
