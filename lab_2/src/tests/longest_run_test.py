from scipy.special import gammaincc

from config.messages import ERRORS


BLOCK_SIZE = 8
SEQ_LEN = 128
NUM_BLOCKS = SEQ_LEN // BLOCK_SIZE
PI_CONSTANTS = [0.2148, 0.3672, 0.2305, 0.1875]


def _stats(bits: str) -> list:
    stats = [0] * 4
    for i in range(0, SEQ_LEN, BLOCK_SIZE):
        block = bits[i:i + BLOCK_SIZE]
        max_subseq = _find_max_subseq(block)

        if max_subseq <= 1:
            stats[0] += 1
        elif max_subseq == 2:
            stats[1] += 1
        elif max_subseq == 3:
            stats[2] += 1
        else:
            stats[3] += 1

    return stats


def _chi_square(stats: list) -> float:
    chi_square = 0

    for v, pi in zip(stats, PI_CONSTANTS):
        chi_square += (v - NUM_BLOCKS * pi) ** 2 / (NUM_BLOCKS * pi)

    return chi_square


def _find_max_subseq(bits: str) -> int:
    max_subseq = 0

    subseq = 0
    for bit in bits:
        if bit == "1":
            subseq += 1
        else:
            max_subseq = max(subseq, max_subseq)
            subseq = 0

    return max(max_subseq, subseq)


def longest_run_test128(bits: str) -> float:
    if len(bits) != SEQ_LEN:
        raise ValueError(ERRORS["invalid_bits_len"].format(seq_len=SEQ_LEN))

    stats = _stats(bits)

    chi_square = _chi_square(stats)

    P_value = gammaincc(1.5, chi_square / 2)

    return P_value
