# Перевести десятичное в двоичную и двоичное в десятичную систему
numb_one = int(input("Enter a decimal number: "))
print(f"In binary: {bin(numb_one)[2:]}")

numb_two = input("Enter binary number: ")
print(f"In decimal: {int(numb_two, base=2)}")

print("-" * 20)


# Написать первую программу: программа должна выводить в консоль несколько строчек
print("Hello, World")
print("It is my first python program")
print("And it is the end of my program")
print("Bye-bye")

print("-" * 20)


# Написать программу на Python, которая запрашивает у пользователя данные и производит расчеты.
user_name = input("Введите ваше имя: ")
print(f"Приветствую, {user_name}!")

travel_distance = float(input("Введите расстояние поездки (km): "))
fuel_consumption = float(input("Введите расход топлива вашего автомобиля на 100км: "))
gasoline_prices = float(input("Введите стоимость 1/литра бензина в вашем регионе: "))

amount_of_gasoline = travel_distance * fuel_consumption / 100
total_coast = gasoline_prices * amount_of_gasoline / 1

print(f"Для поездки вам понадобится {int(amount_of_gasoline)} литров бензина, это будет стоить {int(total_coast)} рублей")