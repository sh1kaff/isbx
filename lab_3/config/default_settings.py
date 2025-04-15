import os

from config.paths import DEFAULT_DIR


_to_default_dir = lambda filename: os.path.join(DEFAULT_DIR, filename)


DEFAULT_SETTINGS = {
    "input_file": _to_default_dir("input_file.txt"),
    "encrypted_input_file": _to_default_dir("encrypted_input_file.txt"),
    "decrypted_input_file": _to_default_dir("decrypted_input_file.txt"),
    "cast5_encrypted_key": _to_default_dir("cast5_encrypted_key.pem"),
    "rsa_public_key": _to_default_dir("rsa_public_key.pem"),
    "rsa_private_key": _to_default_dir("rsa_private_key.pem")
}
