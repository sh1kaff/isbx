from secrets import token_bytes
from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher, modes

from src.atomic.serialization import Serialization
from src.utils import ValidCAST5Utils

from config.crypto_consts import CAST5_PADDING
from config.messages import CRYPTO_ERRORS


class CAST5:
    def __init__(self, key: bytes | None = None, key_bit_len: int = 128):
        if key is not None:
            ValidCAST5Utils.valid_cast5_key(key)
            self.__key = key
            return

        self.__key = gen_cast5_key(key_bit_len)

    @property
    def key(self) -> bytes:
        """Key getter

        Returns:
            bytes: Key
        """
        return self.__key

    @key.setter
    def key(self, k: bytes):
        """Key setter

        Args:
            k (bytes): New key
        """
        ValidCAST5Utils.valid_cast5_key(k)

        self.__key = k

    def serialize(self) -> bytes:
        """Key serializer

        Returns:
            bytes: Serialized key
        """
        return Serialization.serialize_cast5_key(self.key)

    @staticmethod
    def deserialize(serialized_key: bytes) -> bytes:
        """Key deserialized

        Args:
            serialized_key (bytes): Serialized key

        Returns:
            bytes: Original key
        """
        return Serialization.deserialize_cast5_key(serialized_key)

    def encrypt(self, content: bytes) -> bytes:
        """Same with cast5_encrypt_content()"""
        return cast5_encrypt_content(self.key, content)

    def decrypt(self, content: bytes) -> bytes:
        """Same with cast5_decrypt_content()"""
        return cast5_decrypt_content(self.key, content)


def gen_cast5_key(bit_len: int) -> bytes:
    """Generates a CAST5 key

    Args:
        bit_len (int): Key length

    Returns:
        bytes: Generated key
    """
    ValidCAST5Utils.valid_cast5_key_length(bit_len)

    return token_bytes(bit_len // 8)


def cast5_encrypt_content(key: bytes, content: bytes) -> bytes:
    """Encryption with CAST5

    Args:
        key (bytes): CAST5 key
        content (bytes): Content to encryption

    Returns:
        bytes: Ciphertext
    """
    iv = token_bytes(8)

    cipher = Cipher(algorithms.CAST5(key), mode=modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = CAST5_PADDING.padder()

    padded_content = padder.update(content) + padder.finalize()
    encrypted_padded_content = encryptor.update(padded_content) + \
        encryptor.finalize()

    return iv + encrypted_padded_content


def cast5_decrypt_content(
    key: bytes,
    encrypted_padded_content: bytes
) -> bytes:
    """Decryption with CAST5

    Args:
        key (bytes): CAST5 key
        encrypted_padded_content (bytes): Content to decrypt

    Raises:
        ValueError: Wrong key

    Returns:
        bytes: Decrypted content
    """
    iv = encrypted_padded_content[:8]
    encrypted_padded_content = encrypted_padded_content[8:]

    cipher = Cipher(algorithms.CAST5(key), mode=modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = CAST5_PADDING.unpadder()

    try:
        padded_content = decryptor.update(encrypted_padded_content) + \
            decryptor.finalize()
    except ValueError:
        raise ValueError(CRYPTO_ERRORS["decrypt_invalid_cast5"])

    content = unpadder.update(padded_content) + unpadder.finalize()

    return content
