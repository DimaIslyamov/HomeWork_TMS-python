from tasks.task1_map_to_string import convert_numbers_to_string
from tasks.task2_filter_positive import filter_positive
from tasks.task3_filter_palindromes import filter_palindromes
from tasks.task4_timer_decorator import test_timer_decorator
from tasks.task5_flat_area import calculate_flat_area


def main():
    # --- Task 1 ---
    numbers = [1, 2, 3]
    print("Task 1:", convert_numbers_to_string(numbers))

    # --- Task 2 ---
    numbers = [1, 2, -22, 3, -2, 4]
    print("Task 2:", filter_positive(numbers))

    # --- Task 3 ---
    strings = ["abba", "abc", "level", "python", "madam"]
    print("Task 3:", filter_palindromes(strings))

    # --- Task 4 ---
    x = 11
    y = 22
    result = test_timer_decorator(x=x, y=y)
    print("Task 4:", result)

    # --- Task 5 ---
    rooms = [
        {"name": "Kitchen", "length": 6, "width": 4},
        {"name": "Room 1", "length": 5.5, "width": 4.5},
        {"name": "Room 2", "length": 5, "width": 4},
        {"name": "Room 3", "length": 7, "width": 6.3},
    ]

    print("Task 5:", calculate_flat_area(rooms))


if __name__ == "__main__":
    main()