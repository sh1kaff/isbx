import time
import psutil
import multiprocessing as mp

from src.hash_cracker import crack_hash_with_mp


def get_crack_time(
    hash: str,
    last_digits: str,
    bin: str
) -> int:
    real_cores = psutil.cpu_count(logical=False)

    for cores in range(1, int(real_cores * 1.5) + 1):
        start_time = time.time()
        crack_hash_with_mp(hash, last_digits, bin, cores)
        print(f"Time: {time.time() - start_time}")


if __name__ == "__main__":
    get_crack_time("140495200b351b7f18a46e3796f2875ebdf0023568933ef3b99efb285af3f06b","2301", "547905")
