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
    "cast5_key_incr": "The key length should be in 8 bit increments",
    "unsupported_key": "Unsupported key type: {key_type} (only 'public' or 'private')"
}


COMMON_ERRORS = {
    "not_file": "Object {path} is not file!",
    "file_not_json": "File {path} is not JSON!",
    "allowed_methods": "You can use only on of them: {methods}",
    "unsupported_format": "Unsupported file format"
}


HELP = {
    "generate": "Generate keys",
    "encrypt": "Encrypt File",
    "decrypt": "Decrypt File",
    "auto": "Auto Mod (Use Default Settings)",
    "cast5_keylen": "Len of CAST5 key"
}


DESC = {
    "prog_name": "DAMNED ENCRYPTOR",
    "prog_desc": "G.E.D."
}
