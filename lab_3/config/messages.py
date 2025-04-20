WEB_ERRORS = {
    "download_key_not_allowed": "Download key \"{key}\" not allowed!",
    "session_dir_already_created": "Session directory already created!",
    "keys_not_yet_generated": "You haven't generated the keys yet!",
    "invalid_json": "Invalud JSON!",
    "required_param": "Param {param} is required!",
    "no_file_key": "No 'file' key in request!",
    "invalid_upload_filename": "Invalid upload filename!",
    "keys_required": "Required keys: rsa_private_key, cast5_encrypted_key!",
    "invalid_key_pair": "Invalid key pair",
    "max_size": "Max uploaded size: {size}"
}


CRYPTO_ERRORS = {
    "decrypt_invalid_cast5": "Invalid CAST5 key to decrypt",
    "decrypt_invalid_rsa": "Invalid RSA key to decrypt",
    "cast5_key_len": "The key length must be between 40 and 128 bits inclusive",
    "cast5_key_incr": "The key length should be in 8 bit increments"
}


COMMON_ERRORS = {
    "not_file": "Object {path} is not file!",
    "file_not_json": "File {path} is not JSON!"
}