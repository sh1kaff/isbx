from src.atomic.generate import gen_cast5_key
from src.atomic.encrypt import cast5_encrypt_content
from src.atomic.decrypt import cast5_decrypt_content


class CAST5:
    def __init__(self, key_bit_len: int):
        self.key = gen_cast5_key(key_bit_len)


    def encrypt(self, content: bytes) -> bytes:
        return cast5_encrypt_content(self.key, content)


    def decrypt(self, content: bytes) -> bytes:
        return cast5_decrypt_content(self.key, content)
