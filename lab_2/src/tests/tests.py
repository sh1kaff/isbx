from config.messages import ERRORS
from config.config import TESTS

from src.tests.frequency_bit_test import frequency_bit_test
from src.tests.longest_run_test import longest_run_test128
from src.tests.next_bit_test import next_bit_test


def route_test(test: str, bits: str) -> float:
    """Is a router from a string to a test function.

    Args:
        test (str): test identifier string
        bits (str): bits string

    Raises:
        ValueError: the proposed test is not available

    Returns:
        float: test result
    """
    test_funcs = (
        frequency_bit_test,
        longest_run_test128,
        next_bit_test
    )

    test2func = {
        test_key: test_func
        for test_key, test_func
        in zip(TESTS, test_funcs)
    }

    test_func = test2func.get(test)

    if not test_func:
        raise ValueError(ERRORS["invalid_test"].format(test=test))

    result = test_func(bits)

    return result
