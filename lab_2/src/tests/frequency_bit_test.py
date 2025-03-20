import math

from src.utils import valid_bits


def _sum_bits(bits: str) -> int:
    bits_sum = 0
    for bit in bits:
        if bit == "1":
            bits_sum += 1
        else:
            bits_sum -= 1

    return bits_sum


def frequency_bit_test(bits: str) -> float:
    valid_bits(bits)

    N = len(bits)

    S_N = _sum_bits(bits) / math.sqrt(N)

    P_value = math.erfc(abs(S_N) / math.sqrt(2))

    return P_value
