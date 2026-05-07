from exceptions_project.utils import ValidationError


ALLOWED_OPERATIONS = ["+", "-", "*", "/"]


def validate_operation(operation: str):
    if operation not in ALLOWED_OPERATIONS:
        raise ValidationError("Недопустимая операция")


def validate_division(operation: float):
    if operation == 0:
        raise ValidationError("На ноль делить нельзя!")
