value_one = int(input("Введите первое целое число: "))
value_two = int(input("Введите второе целое число: "))
value_three = int(input("Введите третье целое число: "))


def get_result_at_values(val_one: int, val_two: int, val_three: int) -> str:
    result_sum = val_one + val_two + val_three
    difference = val_one - val_two - val_three
    product_of_numbers = val_one * val_two * val_three

    priority_actions_one = (val_one - val_two) + val_three
    priority_actions_two = (val_one * val_two) / val_three
    priority_actions_three = (val_one + val_two) % val_three


    return (f"Сумма: {result_sum}, \n"
            f"Разность: {difference}, \n"
            f"Произведение: {product_of_numbers}, \n"
            f"(a - b) + c: {priority_actions_one}, \n"
            f"(a * b) / c: {round(priority_actions_two, 2)}, \n"
            f"(a + b) % c: {priority_actions_three}, \n")


summ_of_result = get_result_at_values(value_one, value_two, value_three)
print(summ_of_result)