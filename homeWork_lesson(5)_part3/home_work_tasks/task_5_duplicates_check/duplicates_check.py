from home_work_tasks.data import generate_random_list


def get_unic_values(*, input_numbers: list[int]) -> tuple[bool, dict[int, int]]:
    is_unic = len(input_numbers) == len(set(input_numbers))
    counts = {}
    duplicates = {}

    for num in input_numbers:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1

    for value, repeat in counts.items():
        if repeat > 1:
            duplicates[value] = repeat

    return is_unic, duplicates


list_of_rand_values = generate_random_list()
is_unique, duplicates = get_unic_values(input_numbers=list_of_rand_values)

if is_unique:
    print(f"Все элементы уникальны!")
else:
    print(f"Есть дубликаты: {duplicates}")