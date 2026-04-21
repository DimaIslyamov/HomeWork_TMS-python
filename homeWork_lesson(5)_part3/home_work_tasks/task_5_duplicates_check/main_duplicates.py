from home_work_tasks.data import generate_random_list
from home_work_tasks.task_5_duplicates_check.duplicates_check import get_unic_values


list_of_rand_values = generate_random_list()
is_unique, duplicates = get_unic_values(input_numbers=list_of_rand_values)

if is_unique:
    print(f"Все элементы уникальны!")
else:
    print(f"Есть дубликаты: {duplicates}")
