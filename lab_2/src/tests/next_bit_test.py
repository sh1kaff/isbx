import math

from src.utils import valid_bits

def _sign_changes(bits: str, N: int) -> int:
    V_N = 1
    
    for i in range(0, N - 1):
        if bits[i] != bits[i + 1]:
            V_N += 1
    
    return V_N


def _stop_criterion(pi: int, N: int) -> bool:
    condition = abs(pi - 0.5) < 2 / math.sqrt(N)
    return not condition


def _p_value(V_N: float, N: int, pi: float) -> float:
    prob_variance = pi * (1 - pi)

    up = abs(V_N - 2 * N * prob_variance)
    down = 2 * math.sqrt(2 * N) * prob_variance
    
    return math.erfc(up / down)


def next_bit_test(bits: str) -> float:
    valid_bits(bits)

    N = len(bits)

    pi = bits.count("1") / N

    if _stop_criterion(pi, N):
        return 0
    
    V_N = _sign_changes(bits, N)

    if V_N == 0:
        return 0

    return _p_value(V_N, N, pi)


if __name__ == "__main__":
    next_bit_test("010000100101010011001")