import time
from fp_homeWork.utils import is_palindrome
from fp_homeWork.utils import run_time

@run_time
def filter_palindromes(strings: list[str]) -> list[str]:
    time.sleep(1.3)
    return list(filter(is_palindrome, strings))
