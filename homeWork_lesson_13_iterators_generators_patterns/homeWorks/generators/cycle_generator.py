from typing import Generator

# ///// Сделать класс и тут ??
def cycle_generator(values: list[int], limit: int) -> Generator[int, None, None]:
    if limit < 0:
        raise ValueError('limit cannot be negative')

    if not values:
        raise ValueError("values cannot be empty")

    index = 0
    count = 0

    while count < limit:
        yield values[index]

        index += 1
        count += 1

        if index == len(values):
            index = 0

# ///// Отправить в maim.py
try:
    user_input = int(input("Enter a number: "))
    print(list(cycle_generator([1, 2, 3, 4], user_input)))
except ValueError as e:
    print(f"Error: {e}")
