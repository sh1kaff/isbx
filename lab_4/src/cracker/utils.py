import matplotlib.pyplot as plt
from io import BytesIO
import json
import hashlib
import time


def visual_crack_stats(
        cores_stats: list[int],
        crack_time_stats: list[float]
    ) -> BytesIO:
    plt.title("Dependence of hash cracking time on the number of cores involved")
    plt.xlabel("Cores")
    plt.ylabel("Crack Time")

    idx = crack_time_stats.index(min(crack_time_stats))
    minimum = crack_time_stats[idx]

    plt.xticks(range(cores_stats[0], cores_stats[-1] + 1, 1))
    plt.plot(cores_stats, crack_time_stats)
    plt.plot(idx + 1, minimum, marker="o")
    
    buffer = BytesIO()
    plt.savefig(buffer, format="jpg")
    plt.clf()
    plt.close()

    return buffer


def luhn(number: int) -> int:
    rev_dig = map(int, reversed(str(number)))

    summ = 0

    for idx, number in enumerate(rev_dig):
        if idx % 2 == 0:
            number *= 2
            summ += number - 9 if number > 9 else number
        else:
            summ += number

    summ %= 10

    control = (10 - summ) % 10

    return control


def card_correct(
    card: str
) -> bool:
    if len(card) != 16:
        return False
    
    if not card.isdigit():
        return False

    return True


def card_luhn_correct(
    card: str
) -> bool:
    if not card_correct(card):
        return False

    last = int(card[-1])
    control = luhn(int(card[:-1]))

    return control == last


def serialize_card(card: str) -> str:
    if not card_correct(card):
        raise ValueError("Card invalid")
    
    card_info = {
        "bin_code": card[:6],
        "card_number": card[6:12],
        "last": card[12:],
    }

    return json.dumps(card_info)


def hash_alg_correct(hash_alg: str) -> bool:
    if hash_alg in hashlib.algorithms_available:
        return True

    return False


def get_hash_func(hash_alg: str):
    if not hash_alg_correct(hash_alg):
        raise ValueError(f"Incorrect hash {hash_alg}!")
    
    return getattr(hashlib, hash_alg)


def func_time(func, *args, **kwargs) -> tuple[float, str | None]:
    start_time = time.time()
    result = func(*args, **kwargs)
    return (time.time() - start_time, result)
