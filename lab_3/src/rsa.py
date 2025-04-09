from src.atomic.generate import gen_rsa_key_pair
from src.atomic.encrypt import rsa_encrypt_content
from src.atomic.decrypt import rsa_decrypt_content
from src.atomic.serialize import (
    serialize_rsa_public_key,
    serialize_rsa_private_key,
    deserialize_rsa_public_key,
    deserialize_rsa_private_key
)


class RSA:
    def __init__(self):
        key_pair = gen_rsa_key_pair()
        self.public_key = key_pair["public"]
        self.private_key = key_pair["private"]


    def encrypt(self, content: bytes) -> bytes:
        return rsa_encrypt_content(self.public_key, content)


    def decrypt(self, encrypted_content: bytes) -> bytes:
        return rsa_decrypt_content(self.private_key, encrypted_content)


    def serialize(self, key_type: str, filepath: str):
        match key_type:
            case "public":
                serialize_rsa_public_key(self.public_key, filepath)

            case "private":
                serialize_rsa_private_key(self.private_key, filepath)

            case _:
                raise ValueError(f"Unsupported key type: {key_type} (only 'public' or 'private')")


    def deserialize(self, key_type: str, filepath: str) -> bytes:
        match key_type:
            case "public":
                return deserialize_rsa_public_key(filepath)

            case "private":
                return deserialize_rsa_private_key(filepath)

            case _:
                raise ValueError(f"Unsupported key type: {key_type} (only 'public' or 'private')")
