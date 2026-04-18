import random


def generate_random_list(size: int = 10,
                         start: int = 1,
                         end: int = 225) -> list[int]:
    result = []

    for _ in range(size):
        result.append(random.randint(start, end))

    return result
