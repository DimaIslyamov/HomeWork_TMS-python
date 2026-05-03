import time
from typing import Callable


def run_time(func: Callable):
    def wrapper(*args, **kwargs):

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(f"Время выполнения функции: {end - start:.4f} секунд")

        return result
    return wrapper
