import argparse


def valid_args(args: argparse.Namespace):
    count = 0
    methods = ("generate", "encrypt", "decrypt")

    for arg in methods:
        if getattr(args, arg):
            count += 1

    if count > 1:
        raise ValueError(f"You can use only on of them: {methods}")

    elif count == 0:
        raise ValueError(f"One of this settings are must to be!")


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="",
        description=""
    )

    parser.add_argument("--key_bit_len", "-l", type=int, default=128, help="")
    parser.add_argument("--generate", "-g", action="store_true", help="")
    parser.add_argument("--encrypt", "-e", action="store_true", help="")
    parser.add_argument("--decrypt", "-d", action="store_true", help="")
    parser.add_argument("--auto", "-a", action="store_true", help="")

    args = parser.parse_args()
    valid_args(args)

    return args
