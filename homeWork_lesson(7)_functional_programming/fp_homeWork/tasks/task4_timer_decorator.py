import time
from fp_homeWork.utils import run_time


@run_time
def test_timer_decorator(x: int | float, y: int | float) -> int | float:
    time.sleep(1.4)
    return x * y



