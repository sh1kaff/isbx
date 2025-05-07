import logging
import multiprocessing as mp

from src.cracker.utils import get_hash_func
from src.cracker.utils import card_correct
from config.config import DEFAULT_HASH


LIMIT_LEN = 6
"""Number of unknown digits in the card"""
LIMIT = pow(10, LIMIT_LEN)
"""The maximum number minus 1 that can be
on an unknown location in the card """


def _valid_credentials(
    card: str | None = None,
    bin_code: str | None = None,
    last: str | None = None,
):
    """Performs data validation

    Args:
        card (str | None, optional): Card number. Defaults to None.
        bin_code (str | None, optional): BIN code. Defaults to None.
        last (str | None, optional): Last 4 digits of card. Defaults to None.

    Raises:
        ValueError: Incorrect BIN
        ValueError: Incorrect card
        ValueError: Incorrect last digits
    """
    if bin_code is not None and not _bin_correct(bin_code):
        raise ValueError(f"BIN {bin_code} isn't correct!")

    if card is not None and not card_correct(card):
        raise ValueError(f"Card {card} isn't correct!")

    if last is not None and not _last_correct(last):
        raise ValueError(f"Last digits {last} aren't correct!")


def _bin_correct(bin_code: str) -> bool:
    """Performs `bin_code` param validation"""
    if len(bin_code) != 6:
        return False

    if not bin_code.isdigit():
        return False

    return True


def _last_correct(last: str) -> bool:
    """Performs `last` param validation"""
    if len(last) != 4:
        return False

    if not last.isdigit():
        return False

    return True


def card_is_hash(
    card: str,
    target_hash: str,
    hash_alg: str = DEFAULT_HASH,
) -> bool:
    """Checks if the card matches its hash using the `hash_alg` algorithm

    Args:
        card (str): Card number
        target_hash (str): Checked hash
        hash_alg (str, optional): Hashing algorithm. Defaults to DEFAULT_HASH.

    Returns:
        bool: True or False
    """
    _valid_credentials(card=card)
    hash_func = get_hash_func(hash_alg)

    card_bytes = bytes(card, encoding="utf-8")

    return hash_func(card_bytes).hexdigest() == target_hash


def brute_hash(
    target_hash: str,
    last: str,
    bin_code: str,
    start: int = 0,
    end: int | None = None,
    hash_alg: str = DEFAULT_HASH,
) -> str | None:
    """Cracking the hash. It searches the card numbers by mask XXXXXXnnnnnnYYYY, \\
    where: \\
        `last` = "YYYY", \\
        `bin_code` = "XXXXXX". \\
        and `nnnnnn` - numbers from start to end. \\
    For example: \\
        start = 0, end = 666666 \\
        => XXXXXX000000YYYY, XXXXXX000001YYYY, ..., XXXXXX666666YYYY

    Args:
        target_hash (str): Cracking hash
        last (str): Last 4 digits of card
        bin_code (str): BIN of card
        start (int, optional): Beginning of the enumeration. Defaults to 0.
        end (int | None, optional): Ending of the enumeration. Defaults to None.
        hash_alg (str, optional): Hashing algorithm. Defaults to DEFAULT_HASH.

    Raises:
        ValueError: Invalid end param

    Returns:
        str | None: Cracked result or nothing
    """
    _valid_credentials(last=last, bin_code=bin_code)

    if end is None:
        end = LIMIT - 1

    if end > LIMIT - 1:
        raise ValueError("Invalid end param")

    for digits in range(start, end + 1):
        card = bin_code + str(digits).zfill(LIMIT_LEN) + last
        if card_is_hash(card, target_hash, hash_alg):
            return card

    return None


def worker(args) -> str | None:
    """Worker designed to get multithreading up and running properly"""
    target_hash, last, bin_code, start, end, hash_alg = args
    return brute_hash(target_hash, last, bin_code, start, end, hash_alg)


def crack_hash_with_mp(
    target_hash: str,
    last: str,
    bin_code: str,
    hash_alg: str = DEFAULT_HASH,
    cores: int = mp.cpu_count(),
) -> str | None:
    """Multithreaded and automated brute_hash()

    Args:
        target_hash (str): Cracked hash
        last (str): Last 4 digits of card
        bin_code (str): Card BIN
        hash_alg (str, optional): Hashing algorithm. Defaults to DEFAULT_HASH.
        cores (int, optional): Number of cores utilized. Defaults to mp.cpu_count().

    Returns:
        str | None: Cracked result or nothing
    """
    _valid_credentials(last=last, bin_code=bin_code)

    incr = LIMIT // cores
    result = None

    args_gen = (
        (
            target_hash,
            last,
            bin_code,
            (start := incr * core_idx),
            start + incr - 1, hash_alg
        )
        for core_idx in range(0, cores)
    )

    with mp.Pool(processes=cores) as pool:
        logging.info(f"Start multiprocessing. Cores: {cores}")
        logging.info(f"BIN: {bin_code}; Hash: {target_hash}; last: {last}")

        for res in pool.imap_unordered(worker, args_gen):
            if res:
                logging.info(f"Result found! Card: {res}")

                pool.terminate()
                result = res
                break

    return result
