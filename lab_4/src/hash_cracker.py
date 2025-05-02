import logging
import multiprocessing as mp
from hashlib import blake2s


def get_limits(
    bin_code: str,
    last_digits: str
) -> tuple[int, int]:
    limit_len = 16 - len(bin_code) - len(last_digits) 
    limit = pow(10, limit_len)

    return (limit_len, limit)


def card_is_hash(
    card: str,
    target_hash: str
) -> bool:
    if len(card) != 16:
        raise ValueError("Invalid card")

    card_bytes = bytes(card, encoding="utf-8")

    return blake2s(card_bytes).hexdigest() == target_hash


def brute_hash(
    target_hash: str,
    last_digits: str,
    bin_code: str,
    start: int = 0,
    end: int | None = None
) -> str | None:
    limit_len, limit = get_limits(bin_code, last_digits)

    if end is None:
        end = limit - 1

    if end > limit - 1:
        raise ValueError("Invalid end param")

    for digits in range(start, end + 1):
        card = bin_code + str(digits).zfill(limit_len) + last_digits
        if card_is_hash(card, target_hash):
            return card

    return None 


def worker(args) -> str | None:
    target_hash, last_digits, bin_code, start, end = args
    return brute_hash(target_hash, last_digits, bin_code, start, end)


def crack_hash_with_mp(
    target_hash: str,
    last_digits: str,
    bin_code: str,
    cores: int = mp.cpu_count()
) -> str | None:
    limit = get_limits(bin_code, last_digits)[1]
    incr = limit // cores
    result = None

    args_gen = (
        (target_hash, last_digits, bin_code, (start := incr * core_idx), start + incr - 1)
        for core_idx in range(0, cores)
    )

    with mp.Pool(processes=cores) as pool:
        logging.info(f"Start multiprocessing. Cores: {cores}")
        logging.info(f"BIN: {bin_code}; Hash: {target_hash}; last_digits: {last_digits}")

        for res in pool.imap_unordered(worker, args_gen):
            if res:
                logging.info(f"Result found! Card: {res}")

                pool.terminate()
                result = res
                break

    return result
