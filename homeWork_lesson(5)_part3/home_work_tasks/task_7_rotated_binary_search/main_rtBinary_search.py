from home_work_tasks.task_7_rotated_binary_search.rotated_binary_search import rotated_binary_search


# === Ради интереса ===
lenght_of_list = int(input("Какой длины вы хотите список: "))
number_list = []
counter = 1

while len(number_list) < lenght_of_list:
    num = int(input(f"Введите {counter} значение: "))
    number_list.append(num)
    counter += 1

target = int(input(f"У вас есть список {number_list}, "
                   f"какое значение вы хотите найти: "))

index = rotated_binary_search(arr=number_list, target=target)

if index is not None:
    print(f"Значение {target} найдено по индексу {index}")
else:
    print(f"Такого значения нет в списке")


# === Как по задаче ===
# test_list = [5, 6, 7, 1, 2, 3, 4]
# test_target = int(input(f"Какое значение вы хотите найти?: "))
#
# test_index = rotated_binary_search(arr=test_list, target=test_target)
#
# if index is not None:
#     print(f"Значение {test_target} найдено по индексу {test_index}")
#     else:
#     print(f"Такого значения нет в списке")
