import time
import psutil

from typing import Any, Generator

from src.cracker.hash_cracker import crack_hash_with_mp


def func_time(func, *args, **kwargs) -> tuple[float, Any]:
    start_time = time.time()
    result = func(*args, **kwargs)
    return (time.time() - start_time, result)


def get_crack_stats(
    target_hash: str,
    last_digits: str,
    bin_code: str
) -> Generator[dict]:
    real_cores = psutil.cpu_count(logical=False)

    for cores in range(1, int(real_cores * 1.5) + 1):
        crack_time, result = func_time(
            crack_hash_with_mp, target_hash, last_digits, bin_code, cores
        )
        yield {
            "x": cores,
            "y": crack_time,
            "result": result
        }
