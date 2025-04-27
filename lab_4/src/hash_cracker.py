import multiprocessing as mp
from hashlib import blake2s


def get_limits(
    bin: str,
    last_digits: str
) -> tuple[int, int]:
    limit_len = 16 - len(bin) - len(last_digits) 
    limit = pow(10, limit_len)

    return (limit_len, limit)


def card_is_hash(
    card: str,
    hash: str
) -> bool:
    if len(card) != 16:
        raise ValueError("Invalid card")

    card_bytes = bytes(card, encoding="utf-8")

    return blake2s(card_bytes).hexdigest() == hash


def brute_hash(
    hash: str,
    last_digits: str,
    bin: str,
    start: int = 0,
    end: int | None = None
) -> str | None:
    limit_len, limit = get_limits(bin, last_digits)

    if end is None:
        end = limit - 1

    if end > limit - 1:
        raise ValueError("Invalid end param")

    for digits in range(start, end + 1):
        card = bin + str(digits).zfill(limit_len) + last_digits
        if card_is_hash(card, hash):
            return card

    return None 


def worker(args) -> str | None:
    hash, last_digits, bin, start, end = args
    return brute_hash(hash, last_digits, bin, start, end)


def crack_hash_with_mp(
    hash: str,
    last_digits: str,
    bin: str,
    cores: int = mp.cpu_count()
) -> str | None:
    limit = get_limits(bin, last_digits)[1]
    incr = limit // cores
    result = None

    args_iter = (
        (hash, last_digits, bin, (start := incr * core_idx), start + incr - 1)
        for core_idx in range(0, cores)
    )

    with mp.Pool(processes=cores) as p:
        for res in p.map(worker, args_iter):
            if res:
                p.terminate()
                result = res
                break

    return result
