from src.tests.frequency_bit_test import frequency_bit_test
from src.tests.longest_run_test import longest_run_test128
from src.tests.next_bit_test import next_bit_test


def route_test(test: str, bits: str) -> float:
    match test:
        case "freq_bit": test_func = frequency_bit_test
        case "long_run": test_func = longest_run_test128
        case "next_bit": test_func = next_bit_test

    if not test_func:
        raise ValueError("This test don't exist")

    result = test_func(bits)

    return result
