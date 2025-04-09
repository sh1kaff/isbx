import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from secrets import token_bytes

from src.utils import (
    read_bytes,
    write_bytes,
    valid_cast5_key_length
    
)
from config.crypto_globals import CAST5_ENCRYPTED_SERIALIZATION_HEADERS


def gen_cast5_key(bit_len: int) -> bytes:
    valid_cast5_key_length(bit_len)
    
    return token_bytes(bit_len // 8)


def cast5_encrypt_content(key: bytes, content: bytes) -> bytes:
    cipher = Cipher(algorithms.CAST5(key))
    encryptor = cipher.encryptor()

def serialize_cast5_encrypted_key(encrypted_key: bytes, filepath: str):
    headers = CAST5_ENCRYPTED_SERIALIZATION_HEADERS

    content = (
        headers["start"] +
        base64.encodebytes(encrypted_key) +
        headers["end"]
    )

    write_bytes(filepath, content)


def deserialize_cast5_encrypted_key(filepath: str) -> bytes:
    headers = CAST5_ENCRYPTED_SERIALIZATION_HEADERS

    content = read_bytes(filepath)

    if not content.startswith(headers["start"]) or not content.endswith(headers["end"]):
        raise ValueError("Unsupported file format")
    
    encoded_encrypted_key = b"".join(content.split(b"\n")[1:-2])
    encrypted_key = base64.decodebytes(encoded_encrypted_key)

    return encrypted_key
