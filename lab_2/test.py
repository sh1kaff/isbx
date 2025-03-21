import argparse

from src.tests.tests import route_test
from src.utils import get_bits

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Gen'n'Test"
    )

    parser.add_argument("gen_lang", choices=["cpp", "java"])
    parser.add_argument("test", choices=["freq_bit", "long_run", "next_bit"])

    return parser.parse_args()
    

def main():
    args = parse_arguments()

    bits = get_bits(args.gen_lang)

    result = route_test(args.test, bits)

    print(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)