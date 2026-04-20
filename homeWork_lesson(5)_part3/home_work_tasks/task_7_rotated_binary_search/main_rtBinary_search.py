from home_work_tasks.task_7_rotated_binary_search.rotated_binary_search import rotated_binary_search


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
