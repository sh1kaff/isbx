import logging
from src.hash_cracker import crack_hash_with_mp

from config.config import USER_INFO


def main():
    logging.basicConfig(
        level=logging.INFO
    )

    user_info_bin = USER_INFO["bin"]
    for bin in user_info_bin:
        result = crack_hash_with_mp(
            USER_INFO["hash"],
            USER_INFO["last_digits"],
            bin
        )

        if result:
            break

if __name__ == "__main__":
    main()