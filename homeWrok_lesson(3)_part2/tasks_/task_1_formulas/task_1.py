from math import cos, sin, sqrt, pow


def formula_a(a, b) -> float:
    if b == 0:
        raise ValueError("b не может быть равен 0")

    return a**2 / 3 + (a**2 + 4) / b + sqrt((a**2 + 4) / 4) + sqrt((a**2 + 4) ** 3) / 4


def formula_b(x) -> float:
    return cos(x) + sin(x)


def formula_c(x) -> float:
    return (cos(x**2) ** 2 + sin(2 * x - 1) ** 2) ** (1 / 3)


def formula_d(x) -> float:
    return 5 * x + pow(3 * x, 2) * sqrt(1 + sin(x) ** 2)
