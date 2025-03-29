import math

from src.utils import valid_bits


def _sum_bits(bits: str) -> int:
    """Adds bits, with 0 being -1

    Args:
        bits (str): bits string

    Returns:
        int: result sum
    """
    bits_sum = 0
    for bit in bits:
        match bit:
            case "1":
                bits_sum += 1
            case _:
                bits_sum -= 1

    return bits_sum


def frequency_bit_test(bits: str) -> float:
    """The main function for the frequency bit test

    Args:
        bits (str): bits string

    Returns:
        float: test result
    """
    valid_bits(bits)

    seq_len = len(bits)

    norm_sum = _sum_bits(bits) / math.sqrt(seq_len)

    P_value = math.erfc(abs(norm_sum) / math.sqrt(2))

    return P_value
