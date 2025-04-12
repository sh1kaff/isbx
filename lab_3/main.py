from src.atomic.rsa import RSA
from src.atomic.cast5 import CAST5
from src.atomic.hybrid import HybridCryptoSystem

from src.args import get_args
from src.utils import read_json
from config.default_settings import DEFAULT_SETTINGS
from config.common_globals import USER_SETTINGS_FILE


def main():
    args = get_args()

    settings = {}
    if args.auto:
        settings = DEFAULT_SETTINGS
    else:
        settings = read_json(USER_SETTINGS_FILE)


    if args.generate:
        cast5 = CAST5(key_bit_len=args.key_bit_len)
        rsa = RSA()
        hybrid = HybridCryptoSystem(cast5, rsa)

        rsa.serialize("public", settings["rsa_public_key"])
        rsa.serialize("private", settings["rsa_private_key"])
        hybrid.serialize_cast5_encrypted_key(settings["cast5_encrypted_key"])


if __name__ == "__main__":
    main()
