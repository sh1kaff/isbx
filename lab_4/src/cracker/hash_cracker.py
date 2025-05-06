import logging
import multiprocessing as mp

from src.cracker.utils import get_hash_func
from src.cracker.utils import card_correct
from config.config import DEFAULT_HASH


LIMIT_LEN = 6
LIMIT = pow(10, LIMIT_LEN)


def _valid_credentials(
    card: str | None = None,
    bin_code: str | None = None,
    last: str | None = None,
):
    if bin_code is not None and not _bin_correct(bin_code):
        raise ValueError(f"BIN {bin_code} isn't correct!")
    
    if card is not None and not card_correct(card):
        raise ValueError(f"Card {card} isn't correct!")

    if last is not None and not _last_correct(last):
        raise ValueError(f"Last digits {last} aren't correct!")


def _bin_correct(bin_code: str) -> bool:
    if len(bin_code) != 6:
        return False
    
    if not bin_code.isdigit():
        return False

    return True


def _last_correct(last: str) -> bool:
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
    target_hash, last, bin_code, start, end, hash_alg = args
    return brute_hash(target_hash, last, bin_code, start, end, hash_alg)


def crack_hash_with_mp(
    target_hash: str,
    last: str,
    bin_code: str,
    hash_alg: str = DEFAULT_HASH,
    cores: int = mp.cpu_count(),
) -> str | None:
    _valid_credentials(last=last, bin_code=bin_code)

    incr = LIMIT // cores
    result = None


    # args = []
    # for core_idx in range(0, cores):
    #     start = incr * core_idx
    #     args.append((
    #         target_hash,
    #         last,
    #         bin_code,
    #         start,
    #         start + incr - 1, hash_alg
    #     ))

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
