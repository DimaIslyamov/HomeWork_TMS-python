n = int(input("Сумма телефона: "))
k = int(input("Какую сумму вы можете откладывать за день: "))


def count_days_for_masha(*, telephone_sum: int, days_count_sum: int) -> int:
    total: int = 0
    days: int = 0

    while total < telephone_sum:
        days += 1

        if days % 7 != 0:
            total += days_count_sum

    return days


task_2_result = count_days_for_masha(telephone_sum=n, days_count_sum=k)
print(f"Количество дней для Маши: {task_2_result}")
