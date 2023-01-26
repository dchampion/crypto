""" Unit test helper functions """

import concurrent.futures
import inspect
import os
import random
from typing import Iterator


def get_random_bit_lengths(min: int, max: int, step: int = 1) -> list[int]:
    return [_get_random_bit_len(min, max, step) for _ in range(_iterations())]


def _get_random_bit_len(min: int, max: int, step: int = 1) -> int:
    return random.randrange(min, max, step)


def _iterations() -> int:
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
        test_func()
        print(test_info)

    return wrapper

def parallelize(test_func, *args):
    print(f"  {len(*args)} rounds of {test_func.__name__} started in parallel processes")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(test_func, *args)
        process_results(results)
    print(f"  {len(*args)} rounds of {test_func.__name__} finished in parallel processes")
