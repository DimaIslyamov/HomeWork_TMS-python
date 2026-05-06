def get_bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return f"{bmi} Недостаточный вес"
    elif bmi < 25:
        return f"{bmi} Норма"
    elif bmi < 30:
        return f"{bmi} Избыточный вес"
    else:
        return f"{bmi} Ожирение"
