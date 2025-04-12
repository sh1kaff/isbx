import argparse

from src.atomic.rsa import RSA
from src.atomic.cast5 import CAST5


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="",
        description=""
    )

    parser.add_argument("--generate", "-g", help="")
    parser.add_argument("--encrypt", "-e", help="")
    parser.add_argument("--decrypt", "-d", help="")

    return parser.parse_args()


def main():


if __name__ == "__main__":
    main()
