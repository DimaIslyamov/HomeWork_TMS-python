user_int_input = input("Введите трех значное число: ")


if user_int_input.isdigit() and len(user_int_input) == 3:
    number = int(user_int_input)

    # Задание 6. Последняя цифра
    print(number % 10)

    # Задание 7. Количество десятков
    print(number // 10 % 10)

    # Задание 8. Сумма цифр
    print(number // 100 + (number // 10 % 10) + number % 10)

else:
    print("Вы ввели не трех значное число!")

