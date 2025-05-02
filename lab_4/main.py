import logging
from src.hash_cracker import crack_hash_with_mp
from src.crack_time import  get_crack_times

from config.config import USER_INFO


def main():
    logging.basicConfig(
        level=logging.INFO
    )

    # user_info_bin = USER_INFO["bin"]
    # for bin in user_info_bin:
    #     result = crack_hash_with_mp(
    #         USER_INFO["hash"],
    #         USER_INFO["last_digits"],
    #         bin
    #     )

    #     if result:
    #         break
    for x in get_crack_times("a140495200b351b7f18a46e3796f2875ebdf0023568933ef3b99efb285af3f06b","2301", "547905"):
        print(x)

if __name__ == "__main__":
    main()
