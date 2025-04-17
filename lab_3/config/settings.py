import os
from config.paths import DEFAULT_DIR



def gen_settings(base_dir: str) -> dict:
    return {
        filename.split(".")[0]: os.path.join(base_dir, filename)
        for filename in FILENAMES
    }


FILENAMES = (
    "input_file.txt",
    "encrypted_input_file.txt",
    "decrypted_input_file.txt",
    "cast5_encrypted_key.pem",
    "rsa_public_key.pem",
    "rsa_private_key.pem"
)


DEFAULT_SETTINGS = gen_settings(DEFAULT_DIR)
