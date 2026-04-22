import math


def cos_maclaurin(x: float, terms: int) -> float:
    result = 0

    for n in range(terms):
        sign = (-1) ** n
        power = 2 * n

        numerator = x ** power
        denominator = math.factorial(power)

        result += sign * (numerator / denominator)

    return result


# пример
x = 1  # радианы!
terms = 10

approx = cos_maclaurin(x, terms)
real = math.cos(x)

print(f"Наш результат cos: {approx}")
print(f"Настоящий cos: {real}")
