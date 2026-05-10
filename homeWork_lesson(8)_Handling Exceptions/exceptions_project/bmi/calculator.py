from exceptions_project.utils.exceptions import ValidationError


def calculate_bmi(height: float, weight: float) -> float:
    if height <= 0:
        raise ValidationError("Рост должен быть больше 0")

    if weight <= 0:
        raise ValidationError("Вес должен быть больше 0")

    return weight / (height ** 2)
