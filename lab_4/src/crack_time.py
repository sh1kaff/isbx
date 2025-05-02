import time
import psutil
import multiprocessing as mp

from typing import Any

from src.hash_cracker import crack_hash_with_mp


def func_time(func, *args, **kwargs) -> tuple[float, Any]:
    start_time = time.time()
    result = func(*args, **kwargs)
    return (time.time() - start_time, result)


def get_crack_time(
    target_hash: str,
    last_digits: str,
    bin_code: str
):
    real_cores = psutil.cpu_count(logical=False)

    for cores in range(1, int(real_cores * 1.5) + 1):
        crack_time, result = func_time(
            crack_hash_with_mp, target_hash, last_digits, bin_code, cores
        )
        


if __name__ == "__main__":
    get_crack_time("140495200b351b7f18a46e3796f2875ebdf0023568933ef3b99efb285af3f06b","2301", "547905")
