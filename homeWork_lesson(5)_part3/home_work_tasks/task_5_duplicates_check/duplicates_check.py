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



