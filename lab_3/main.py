import argparse

from src.atomic.rsa import RSA
from src.atomic.cast5 import CAST5


def valid_args(args: argparse.Namespace):
    count = 0
    methods = ("generate", "encrypt", "decrypt")

    for arg in methods:
        if getattr(args, arg) is not None:
            count += 1

    if count > 1:
            raise ValueError(f"You can use only on of them: {methods}")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="",
        description=""
    )

    parser.add_argument("--generate", "-g", help="")
    parser.add_argument("--encrypt", "-e", help="")
    parser.add_argument("--decrypt", "-d", help="")

    args = parser.parse_args()
    valid_args(args)

    return args


def main():
    args = get_args()

    print(args)

if __name__ == "__main__":
    main()
