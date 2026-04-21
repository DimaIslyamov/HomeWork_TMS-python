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
