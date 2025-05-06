import psutil

from typing import Any, Generator

from src.cracker.hash_cracker import crack_hash_with_mp
from src.cracker.utils import func_time
from config.config import DEFAULT_HASH


def get_crack_stats(
    target_hash: str,
    last: str,
    bin_code: str,
    hash_alg: str = DEFAULT_HASH,
) -> Generator[dict[str, Any], Any, Any]:
    """Computing cracking statistics, or full pass statistics across all map variants. 

    Args:
        target_hash (str): Cracking hash
        last (str): Last 4 card digits
        bin_code (str): Card BIN
        hash_alg (str, optional): Hashing algorithm. Defaults to DEFAULT_HASH.

    Yields:
        Generator[dict[str, Any], Any, Any]: Stats dict
    """
    real_cores = psutil.cpu_count(logical=False)

    for cores in range(1, int(real_cores * 1.5) + 1):
        crack_time, result = func_time(
            crack_hash_with_mp, target_hash, last, bin_code, hash_alg, cores,
        )
        yield {
            "cores": cores,
            "crack_time": crack_time,
            "result": result
        }
