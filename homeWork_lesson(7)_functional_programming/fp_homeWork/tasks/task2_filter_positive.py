import time
from fp_homeWork.utils import run_time


@run_time
def filter_positive(numbers: list[int]) -> list[int]:
    time.sleep(1.1)
    return list(filter(lambda x: x > 0, numbers))
