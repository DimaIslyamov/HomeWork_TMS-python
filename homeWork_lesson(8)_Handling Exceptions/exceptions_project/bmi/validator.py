from exceptions_project.utils import ValidationError


MIN_HEIGHT = 0
MAX_HEIGHT = 2.5

MIN_WEIGHT = 0
MAX_WEIGHT = 150

# - Тут явно можно оптимизировать и сделать одну функцию
# def validate_positive(value, field_name): или def validate_range(value, min_value, max_value, field_name):

def validate_height(value: float):
    if value <= MIN_HEIGHT:
        raise ValidationError("Рост не может быть '0'!")
    if value > MAX_HEIGHT:
        raise ValidationError("Кто ты животное!?")


def validate_weight(value: float):
    if value <= MIN_WEIGHT:
        raise ValidationError("Легкий как перышко")
    if value > MAX_WEIGHT :
        raise ValidationError("Тебя уже колоть пора!")
