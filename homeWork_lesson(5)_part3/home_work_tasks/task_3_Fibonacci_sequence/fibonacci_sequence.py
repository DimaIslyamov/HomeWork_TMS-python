def fibonacci_sequence(*, value: int) -> list[int]:
    result = [1, 1]

    if value <= 0:
        return []
    elif value == 1:
        return [1]

    for _ in range(3, value + 1):
        result.append(result[-1] + result[-2])

    return result


user_input_value = int(input("Enter a number: "))
sequence = fibonacci_sequence(value=user_input_value)
print(sequence)


# ==== Вариант первый (тестовый) ====
# def fibonacci(*, user_value: int):
#     a = 1
#     b = 1
#
#     if user_value == 0:
#         print(1)
#         return
#     else:
#         print(a, b, end=" ")
#
#         for _ in range(3, user_value + 1):
#             c = a + b
#             print(c, end=" ")
#             a = b
#             b = c
#
#
# fibonacci(user_value=user_input_value)
