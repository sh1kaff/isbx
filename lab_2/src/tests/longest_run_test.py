from scipy.special import gammaincc

from config.constants import LONGEST_RUN_CONSTS
from config.messages import ERRORS


def _stats(bits: str) -> list:
    seq_len = LONGEST_RUN_CONSTS["SEQ_LEN"]
    block_size = LONGEST_RUN_CONSTS["BLOCK_SIZE"]

    stats = [0] * 4

    for i in range(0, seq_len, block_size):
        block = bits[i:i + block_size]
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
    num_blocks = LONGEST_RUN_CONSTS["NUM_BLOCKS"]
    pi_constants = LONGEST_RUN_CONSTS["PI_CONSTANTS"]

    chi_square = 0

    for v, pi in zip(stats, pi_constants):
        chi_square += (v - num_blocks * pi) ** 2 / (num_blocks * pi)

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
    seq_len = LONGEST_RUN_CONSTS["SEQ_LEN"]

    if len(bits) != seq_len:
        raise ValueError(ERRORS["invalid_bits_len"].format(seq_len=seq_len))

    stats = _stats(bits)

    chi_square = _chi_square(stats)

    P_value = gammaincc(1.5, chi_square / 2)

    return P_value
