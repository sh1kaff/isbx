import math

from src.utils import valid_bits


def _sign_changes(bits: str) -> int:
    """Counts the number of bit changes in a bit string

    Args:
        bits (str): bits string

    Returns:
        int: sign changes count
    """
    seq_len = len(bits)

    sign_changes = 1
    for i in range(0, seq_len - 1):
        if bits[i] != bits[i + 1]:
            sign_changes += 1

    return sign_changes


def _stop_criterion(ones_ratio: int, seq_len: int) -> bool:
    """Exit condition from the test

    Args:
        ones_ratio (int): percentage of ones in a bit string
        seq_len (int): bits count

    Returns:
        bool: whether the stop condition has been triggered or not
    """
    condition = abs(ones_ratio - 0.5) < 2 / math.sqrt(seq_len)
    return not condition


def _p_value(sign_changes: float, seq_len: int, ones_ratio: float) -> float:
    """Calculating the P value for a test

    Args:
        sign_changes (float): sign changes count
        seq_len (int): bits count
        ones_ratio (float): percentage of ones in a bit string

    Returns:
        float: test result
    """
    prob_variance = ones_ratio * (1 - ones_ratio)

    if prob_variance == 0:
        return 0

    up = abs(sign_changes - 2 * seq_len * prob_variance)
    down = 2 * math.sqrt(2 * seq_len) * prob_variance

    return math.erfc(up / down)


def next_bit_test(bits: str) -> float:
    """Main function for the next-bit test

    Args:
        bits (str): bits string

    Returns:
        float: test result
    """
    valid_bits(bits)

    seq_len = len(bits)

    ones_ratio = bits.count("1") / seq_len

    if _stop_criterion(ones_ratio, seq_len):
        return 0

    sign_changes = _sign_changes(bits)

    P_value = _p_value(sign_changes, seq_len, ones_ratio)

    return P_value
