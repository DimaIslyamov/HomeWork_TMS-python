from home_work_tasks.data import generate_random_list


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


value_list = generate_random_list()
total, minimum, maximum = get_list_stats(input_list=value_list)

task_4_result = (f"Total: {total}\n"
               f"Minimum: {minimum}\n"
               f"Maximum: {maximum}")

print(task_4_result)

# === Функция через использование встроенных методов ===
# def get_list_stats(*, input_list: list[int]) -> tuple[int, int, int]:
#     total = sum(input_list)
#     minimum = min(input_list)
#     maximum = max(input_list)
#
#     return total, minimum, maximum
