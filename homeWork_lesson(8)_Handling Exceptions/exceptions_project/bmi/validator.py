from exceptions_project.utils import ValidationError


def validate_height(value: float):
    if value <= 0:
        raise ValidationError("Рост не может быть '0'!")
    if value > 2.5:
        raise ValidationError("Кто ты животное!?")


def validate_weight(value: float):
    if value <= 0:
        raise ValidationError("Легкий как перышко")
    if value > 150 :
        raise ValidationError("Тебя уже колоть пора!")
