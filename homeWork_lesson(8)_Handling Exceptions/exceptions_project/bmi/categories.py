from enum import Enum


class BMICategory(Enum):
    UNDERWEIGHT = "Недостаточный вес"
    NORMAL = "Нормальный вес"
    OVERWEIGHT = "Избыточный вес"
    OBESE = "Ожирение"


BMI_RANGES = {
    BMICategory.UNDERWEIGHT: lambda bmi: bmi < 18.5,
    BMICategory.NORMAL: lambda bmi: 18.5 <= bmi < 25,
    BMICategory.OVERWEIGHT: lambda bmi: 25 <= bmi < 30,
    BMICategory.OBESE: lambda bmi: bmi >= 30,
}


def get_bmi_category(bmi: float) -> BMICategory | None:
    for category, value in BMI_RANGES.items():

        if value(bmi):
            return category

    return None
