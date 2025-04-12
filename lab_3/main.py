from src.atomic.rsa import RSA
from src.atomic.cast5 import CAST5
from src.atomic.hybrid import *

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

        rsa.serialize("public", settings["rsa_public_key"])
        rsa.serialize("private", settings["rsa_private_key"])

        cast5_encrypted_key = rsa_encrypt_cast5_key(rsa.public_key, cast5.key)
        serialize_cast5_encrypted_key(cast5_encrypted_key, settings["cast5_encrypted_key"])

    elif args.encrypt:
        rsa = RSA(
            private_key=RSA.deserialize("private", settings["rsa_private_key"])
        )

        cast5_encrypted_key = deserialize_cast5_encrypted_key(
            settings["cast5_encrypted_key"]
        )
        cast5 = CAST5(
            key=rsa_decrypt_cast5_key(rsa.private_key, cast5_encrypted_key)
        )

        encrypted_content = cast5.encrypt(
            read_bytes(settings["input_file"])
        )
        write_bytes(
            settings["encrypted_input_file"],
            encrypted_content
        )
        
    elif args.decrypt:
        rsa = RSA(
            private_key=RSA.deserialize("private", settings["rsa_private_key"])
        )

        cast5_encrypted_key = deserialize_cast5_encrypted_key(
            settings["cast5_encrypted_key"]
        )
        cast5 = CAST5(
            key=rsa_decrypt_cast5_key(rsa.private_key, cast5_encrypted_key)
        )

        decrypted_content = cast5.decrypt(
            read_bytes(settings["encrypted_input_file"])
        )
        write_bytes(
            settings["decrypted_input_file"],
            decrypted_content
        )

if __name__ == "__main__":
    main()
