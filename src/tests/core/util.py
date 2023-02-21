""" Unit test helper functions """

import concurrent.futures
import inspect
import os
import random
import time
from typing import Iterator


def random_ranges(min: int, max: int, step: int = 1) -> list[int]:
    return [random_range(min, max, step) for _ in range(num_cores())]


def random_range(min: int, max: int, step: int = 1) -> int:
    return random.randrange(min, max, step)


def num_cores() -> int:
    num_cores = _num_cores()
    return 4 if (num_cores is None or num_cores < 4) else num_cores


def _num_cores() -> int | None:
    return os.cpu_count()


def process_results(results: Iterator) -> None:
    for result in results:
        if result is not None:
            print(result)

def test_log(test_func):

    if len(inspect.getfullargspec(test_func).args) > 0:
        return test_func

    def wrapper():
        if test_func.__name__ == "main":
            test_info = f"all tests in {test_func.__module__}"
            print(f"running {test_info}")
            test_info = f"finished {test_info}"
        else:
            test_info = f"{test_func.__name__} passed"
        t0 = time.time_ns()
        test_func()
        t1 = time.time_ns()
        print(f"{test_info} ({round((t1-t0)/1000000, 2)} ms)")

    return wrapper

def parallelize(test_func, *args):
    print(f"  {len(*args)} rounds of {test_func.__name__} started in parallel processes")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(test_func, *args)
        process_results(results)
    print(f"  {len(*args)} rounds of {test_func.__name__} finished in parallel processes")
