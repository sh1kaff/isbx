import argparse

from config.messages import (
    COMMON_ERRORS,
    HELP,
    DESC
)


class Args:
    @staticmethod
    def valid_args(args: argparse.Namespace):
        """Checks CLI arguments

        Args:
            args (argparse.Namespace): Arguments

        Raises:
            ValueError: Unauthorized methods
            ValueError: Methods required
        """
        count = 0
        methods = ("generate", "encrypt", "decrypt")

        for arg in methods:
            if getattr(args, arg):
                count += 1

        if count > 1:
            raise ValueError(
                COMMON_ERRORS["allowed_methods"].format(methods=methods)
            )

        elif count == 0:
            raise ValueError(COMMON_ERRORS["necess_methods"])

    @staticmethod
    def get_args() -> argparse.Namespace:
        """Gets arguments from the input

        Returns:
            argparse.Namespace: Arguments namespace
        """
        parser = argparse.ArgumentParser(
            prog=DESC["prog_name"],
            description=DESC["prog_desc"]
        )

        parser.add_argument(
            "--cast5_keylen",
            "-cl",
            type=int,
            default=128,
            help=HELP["cast5_keylen"]
        )
        parser.add_argument("--generate", "-g", action="store_true", help=HELP["generate"])
        parser.add_argument("--encrypt", "-e", action="store_true", help=HELP["encrypt"])
        parser.add_argument("--decrypt", "-d", action="store_true", help=HELP["decrypt"])
        parser.add_argument("--auto", "-a", action="store_true", help=HELP["auto"])

        args = parser.parse_args()
        Args.valid_args(args)

        return args
