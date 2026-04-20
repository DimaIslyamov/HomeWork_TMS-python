def rotated_binary_search(*, arr: list[int], target: int) -> int | None:
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid

        # левая часть отсортирована
        if arr[low] <= arr[mid]:
            if arr[low] <= target < arr[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            # правая часть отсортирована
            if arr[mid] < target <= arr[high]:
                low = mid + 1
            else:
                high = mid - 1

    return None
