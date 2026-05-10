from exceptions_project.bmi.constants import (
    MAX_HEIGHT,
    MAX_WEIGHT,
    MIN_HEIGHT,
    MIN_WEIGHT,
)
from exceptions_project.bmi.input_handler import get_float_input
from exceptions_project.bmi.categories import get_bmi_category
from exceptions_project.bmi.calculator import calculate_bmi
from exceptions_project.bmi.validator import validator_range


def process_bmi():
    height = get_float_input("Введите рост (м): ")
    weight = get_float_input("Введите вес (кг): ")

    validator_range(
        value=height,
        min_val=MIN_HEIGHT,
        max_val=MAX_HEIGHT,
        field_str="Рост"
    )

    validator_range(
        value=weight,
        min_val=MIN_WEIGHT,
        max_val=MAX_WEIGHT,
        field_str="Вес"
    )

    bmi = calculate_bmi(height, weight)
    category = get_bmi_category(bmi)

    return bmi, category
