import os

from config.common_globals import DEFAULT_DIR


DEFAULT_SETTINGS = {
    "input_file": os.path.join(DEFAULT_DIR, "input_file.txt"),
    "encrypted_input_file": os.path.join(DEFAULT_DIR, "encrypted_input_file.txt"),
    "decrypted_input_file": os.path.join(DEFAULT_DIR, "decrypted_input_file.txt"),
    "cast5_encrypted_key": os.path.join(DEFAULT_DIR, "cast5_encrypted_key.pem"),
    "rsa_public_key": os.path.join(DEFAULT_DIR, "rsa_public_key.pem"),
    "rsa_private_key": os.path.join(DEFAULT_DIR, "rsa_private_key.pem")
}
