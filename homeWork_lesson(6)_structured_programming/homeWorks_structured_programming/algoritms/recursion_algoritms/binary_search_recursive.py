def binary_search_recursive(arr: list[int], target: int,
                            low: int, high: int) -> int | None:
    if low > high:
        return None

    mid =  (low + high) // 2
    guess = arr[mid]

    if guess == target:
        return mid
    elif guess > target:
        return binary_search_recursive(arr, target, low, mid - 1)
    else:
        return binary_search_recursive(arr, target, mid + 1, high)


array_range = range(1, 20)
target_value = 6

index = binary_search_recursive(list(array_range), target_value,
                                0, len(array_range) - 1)
print(index)
