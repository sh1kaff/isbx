from src.tests.frequency_bit_test import frequency_bit_test
from src.tests.longest_run_test import longest_run_test128
from src.tests.next_bit_test import next_bit_test


str2test = {
    "freq_bit": frequency_bit_test,
    "long_run": longest_run_test128,
    "next_bit": next_bit_test
}


def route_test(test: str, bits: str) -> float:
    test_func = str2test.get(test)
    if not test_func:
        raise ValueError("This test don't exist")

    result = test_func(bits)

    return result
