from home_work_tasks.data import generate_random_list
from home_work_tasks.task_6_binary_search_index.binary_serch_index import binary_search_index


test_list = sorted(generate_random_list())
print(f"Список: {test_list}")

target_value = int(input(f"Значение для поиска его индекса: "))

task_6_index = binary_search_index(arr=test_list, target=target_value)

if task_6_index is not None:
    print(f"Значение {target_value} найдено по индексу {task_6_index}")
else:
    print(f"Значение {target_value} не найдено в списке")
