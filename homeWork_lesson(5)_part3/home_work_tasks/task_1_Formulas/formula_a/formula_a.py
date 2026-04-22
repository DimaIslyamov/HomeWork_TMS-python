import math


def sin_maclaurin(x: float, terms: int) -> float:
    result = 0

    for n in range(terms):
        sign = (-1) ** n
        power = 2 * n + 1

        numerator = x ** power
        denominator = math.factorial(power)

        result += sign * (numerator / denominator)

    return result


# пример
x = 1  # радианы!
terms = 10

approx = sin_maclaurin(x, terms)
real = math.sin(x)

print(f"Наш результат sin: {approx}")
print(f"Настоящий sin: {real}")
