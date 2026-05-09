def calculate_bmi(height: float, weight: float) -> float:
    assert height > 0
    assert weight > 0

    return weight / (height ** 2)
