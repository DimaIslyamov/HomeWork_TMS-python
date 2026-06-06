from typing import Generator

# /// Сделать класс фибоначи ?
def fibonacci_sequence(limit: int) -> Generator[int, None, None]:
    if limit < 0:
        raise ValueError("Limit cannot be negative")

    first, second = 1, 1

    for _ in range(limit):
        yield first
        first, second = second, first + second


# //// практика вывода класса - для дальнейшего использования в main.py
try:
    user_input = int(input("Enter a number: "))
    print(list(fibonacci_sequence(user_input)))
except ValueError as error:
    print(f"Error: {error}")
