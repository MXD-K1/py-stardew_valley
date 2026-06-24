from time import perf_counter
from typing import Callable


def time(func: Callable):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        func(*args, **kwargs)
        elapsed_time = perf_counter() - start
        print(elapsed_time)
    return wrapper
