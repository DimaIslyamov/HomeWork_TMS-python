from exceptions_project.utils import ValidationError


def validator_range(value: float, min_val: float, max_val: float, field_str: str):
    if value < min_val:
        raise ValidationError(f"{field_str} не может быть меньше {min_val}")

    if value > max_val:
        raise ValidationError(f'{field_str} не может быть больше {max_val}')
