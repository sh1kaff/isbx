from secrets import token_bytes
from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher, modes

from src.utils import valid_cast5_key_length, valid_cast5_key
from config.crypto_consts import CAST5_PADDING


class CAST5:
    def __init__(self, key: bytes | None = None, key_bit_len: int = 128):
        if key is not None:
            valid_cast5_key(key)
            self.key = key
            return
    
        self.key = gen_cast5_key(key_bit_len)


    def encrypt(self, content: bytes) -> bytes:
        return cast5_encrypt_content(self.key, content)


    def decrypt(self, content: bytes) -> bytes:
        return cast5_decrypt_content(self.key, content)


def gen_cast5_key(bit_len: int) -> bytes:
    valid_cast5_key_length(bit_len)
    
    return token_bytes(bit_len // 8)


def cast5_encrypt_content(key: bytes, content: bytes) -> bytes:
    iv = token_bytes(8)

    cipher = Cipher(algorithms.CAST5(key), mode=modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = CAST5_PADDING.padder()

    padded_content = padder.update(content) + padder.finalize()
    encrypted_padded_content = encryptor.update(padded_content) + encryptor.finalize()

    return iv + encrypted_padded_content


def cast5_decrypt_content(key: bytes, encrypted_padded_content: bytes) -> bytes:
    # error handler
    iv = encrypted_padded_content[:8]
    encrypted_padded_content = encrypted_padded_content[8:]

    cipher = Cipher(algorithms.CAST5(key), mode=modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = CAST5_PADDING.unpadder()

    padded_content = decryptor.update(encrypted_padded_content) + decryptor.finalize()
    content = unpadder.update(padded_content) + unpadder.finalize()

    return content
