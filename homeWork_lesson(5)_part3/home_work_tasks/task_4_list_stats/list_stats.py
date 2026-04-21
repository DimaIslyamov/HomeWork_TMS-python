def get_list_stats(*, input_list: list[int]) -> tuple:
    count: int = 0
    min_value = input_list[0]
    max_value = input_list[0]

    for value in input_list:
        count += value

        if value < min_value:
            min_value = value

        if value > max_value:
            max_value = value

    return count, min_value, max_value


# === Функция через использование встроенных методов ===
# def get_list_stats(*, input_list: list[int]) -> tuple[int, int, int]:
#     total = sum(input_list)
#     minimum = min(input_list)
#     maximum = max(input_list)
#
#     return total, minimum, maximum
