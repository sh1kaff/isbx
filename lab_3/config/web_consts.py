ALLOWED_DOWNLOAD_KEYS = (
    "rsa_private_key",
    "rsa_public_key",
    "cast5_encrypted_key"
)


ALLOWED_FILENAMES = (
    "input_file",
    "encrypted_input_file",
    "decrypted_input_file"
)


WEB_ERRORS = {
    "download_key_not_allowed": "Download key \"{key}\" not allowed!",
    "session_dir_already_created": "Session directory already created!",
    "keys_not_yet_generated": "You haven't generated the keys yet!",
    "invalid_json": "Invalud JSON!",
    "required_param": "Param {param} is required!",
    "no_file_key": "No 'file' key in request!"
}
