import time
from fp_homeWork.utils import run_time

@run_time
def convert_numbers_to_string(numbers: list[int]) -> list[str]:
    time.sleep(1)
    return list(map(lambda x: str(x), numbers))

