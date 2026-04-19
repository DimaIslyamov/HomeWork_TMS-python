from home_work_tasks.data import generate_random_list


def binary_search_index(*, arr: list[int], target: int) -> int | None:
    low: int = 0
    high = len(arr) - 1

    while low <= high:
        mid_index = (low + high) // 2
        mid_value = arr[mid_index]

        if mid_value == target:
            return mid_index
        elif mid_value > target:
            high = mid_index - 1
        else:
            low = mid_index + 1

    return None


test_list = sorted(generate_random_list())
print(f"Список: {test_list}")

target_value = int(input(f"Значение для поиска его индекса: "))

task_6_index = binary_search_index(arr=test_list, target=target_value)

if task_6_index is not None:
    print(f"Значение {target_value} найдено по индексу {task_6_index}")
else:
    print(f"Значение {target_value} не найдено в списке")
