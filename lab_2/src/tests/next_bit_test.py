import math

from src.utils import valid_bits


def _sign_changes(bits: str) -> int:
    seq_len = len(bits)

    sign_changes = 1
    for i in range(0, seq_len - 1):
        if bits[i] != bits[i + 1]:
            sign_changes += 1

    return sign_changes


def _stop_criterion(ones_ratio: int, seq_len: int) -> bool:
    condition = abs(ones_ratio - 0.5) < 2 / math.sqrt(seq_len)
    return not condition


def _p_value(sign_changes: float, seq_len: int, ones_ratio: float) -> float:
    prob_variance = ones_ratio * (1 - ones_ratio)

    up = abs(sign_changes - 2 * seq_len * prob_variance)
    down = 2 * math.sqrt(2 * seq_len) * prob_variance

    return math.erfc(up / down)


def next_bit_test(bits: str) -> float:
    valid_bits(bits)

    seq_len = len(bits)

    ones_ratio = bits.count("1") / seq_len

    if _stop_criterion(ones_ratio, seq_len):
        return 0

    sign_changes = _sign_changes(bits)

    if sign_changes == 0:
        return 0

    P_value = _p_value(sign_changes, seq_len, ones_ratio)

    print(f"{seq_len=}\n{ones_ratio=}\n{sign_changes=}\n{P_value=}")

    return P_value
