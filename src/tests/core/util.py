""" Unit test helper functions """

import random
import os
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
