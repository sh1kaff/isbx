import argparse

from config.messages import MESSAGES, DESCRIPTIONS
from config.config import LANGS, TESTS

from src.tests.tests import route_test
from src.utils import get_bits


def parse_arguments() -> argparse.Namespace:
    """Parse arguments from command line.

    Returns:
        argparse.Namespace: arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="Gen'n'Test",
        description=DESCRIPTIONS["program"]
    )

    parser.add_argument(
        "gen_lang",
        choices=LANGS,
        help=DESCRIPTIONS["gen_lang"]
    )

    parser.add_argument(
        "tests",
        nargs="*",
        choices=TESTS,
        help=DESCRIPTIONS["tests"]
    )

    return parser.parse_args()


def main():
    """Progam Entry Point"""
    args = parse_arguments()

    bits = get_bits(args.gen_lang)

    print(MESSAGES["what_lang"].format(lang=args.gen_lang))
    print(MESSAGES["bits_result"].format(bits=bits), end="\n\n")

    if not args.tests:
        args.tests = TESTS

    for test in args.tests:
        result = route_test(test, bits)

        status = "Passed" if result >= 0.01 and result <= 1 else "Failed"

        print(MESSAGES["test_result"].format(test=test, result=result))
        print(MESSAGES["status"].format(status=status), end="\n\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
