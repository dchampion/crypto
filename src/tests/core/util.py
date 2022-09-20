import random
import os


def get_random_bit_lengths(min: int, max: int, step: int = 1) -> list[int]:
    return [get_random_bit_len(min, max, step) for _ in range(_iterations())]


def get_random_bit_len(min: int, max: int, step: int = 1) -> int:
    return random.randrange(min, max, step)


def _iterations() -> int:
    num_cores = _num_cores()
    return 4 if num_cores < 4 else num_cores


def _num_cores() -> int:
    return os.cpu_count()


def process_results(results):
    for result in results:
        if result is not None:
            print(result)
