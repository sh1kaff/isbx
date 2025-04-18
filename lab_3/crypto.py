from src.atomic.hybrid import HybridCryptoSystem

from src.args import Args
from src.utils import IOUtils
from config.settings import DEFAULT_SETTINGS
from config.paths import USER_SETTINGS_FILE


def main():
    args = Args.get_args()

    settings = {}
    if args.auto:
        settings = DEFAULT_SETTINGS
    else:
        settings = IOUtils.read_json(USER_SETTINGS_FILE)


    if args.generate:
        hybrid = HybridCryptoSystem(cast5_keylen=args.cast5_keylen)

        hybrid.serialize_keys_to_files(
            settings["rsa_private_key"],
            settings["rsa_public_key"],
            settings["cast5_encrypted_key"]
        )

        return


    if args.encrypt or args.decrypt:
        hybrid = HybridCryptoSystem()
        hybrid.import_keys_from_files(
            settings["rsa_private_key"],
            settings["cast5_encrypted_key"]
        )

    if args.encrypt:
        hybrid.encrypt_content(
            settings["input_file"],
            settings["encrypted_input_file"]
        )
        
    elif args.decrypt:
        hybrid.decrypt_content(
            settings["encrypted_input_file"],
            settings["decrypted_input_file"]
        )


if __name__ == "__main__":
    main()
