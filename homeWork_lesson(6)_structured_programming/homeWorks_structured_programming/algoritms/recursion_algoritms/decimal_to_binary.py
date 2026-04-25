# === Рекурсивный вариант ===
def decimal_to_bin(decimal_value: int) -> str:
    if decimal_value < 2:
        return str(decimal_value)

    return decimal_to_bin(decimal_value // 2) + str(decimal_value % 2)


# === Итеративный вариант ===
def decimal_to_bin_iterative(decimal_value: int) -> str:
    dec_str = ""

    while decimal_value > 0:
        dec_str += str(decimal_value % 2)
        decimal_value //= 2

    return dec_str[::-1]


# === Запуск обоих вариантов ===
user_value = int(input("Введите десятичное значение: "))

variant_1 = decimal_to_bin(user_value)
variant_2 = decimal_to_bin_iterative(user_value)

print(f"Через рекурсию - {variant_1}, Через Итеративный вариант - {variant_2}")
