import math

from src.utils import valid_bits


def _sum_bits(bits: str) -> int:
    bits_sum = 0
    for bit in bits:
        match bit:
            case "1": bits_sum += 1
            case "0": bits_sum -= 1
    
    return bits_sum


def frequency_bit_test(bits: str) -> float:
    valid_bits(bits)

    N = len(bits)

    bits_sum = _sum_bits(bits)

    S_N = bits_sum / math.sqrt(N)

    P_value = math.erfc(abs(S_N) / math.sqrt(2))

    return P_value

if __name__ == "__main__":
    print( frequency_bit_test("") )
