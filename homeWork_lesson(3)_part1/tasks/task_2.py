from math import sqrt

cat_a = float(input("Введите Первый катет: "))
cat_b = float(input("Введите Второй катет: "))

area: float = (cat_a * cat_b) / 2
hypotenuse: float = sqrt((cat_a ** 2) + (cat_b ** 2))

print(f"Площадь треугольника равна: {area}, его гипотенуза: {hypotenuse:.2f} ")