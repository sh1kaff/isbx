from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from src.atomic.serialization import Serialization
from config.crypto_consts import RSA_PADDING

# убрать все импорты в cast5 и rsa и сделать, чтобы более сложные операции выполняла HCS, а rsa&cast5 делала только самую базу

class RSA:
    def __init__(self, private_key: RSAPrivateKey | None = None):
        if private_key is not None:
            self.__private_key = private_key
            self.__public_key = private_key.public_key()
            return

        key_pair = gen_rsa_key_pair()
        self.__public_key = key_pair["public"]
        self.__private_key = key_pair["private"]


    @property
    def public_key(self) -> RSAPublicKey:
        return self.__public_key


    @property
    def private_key(self) -> RSAPrivateKey:
        return self.__private_key


    @private_key.setter
    def private_key(self, priv_key: RSAPrivateKey):
        self.__private_key = priv_key
        self.__public_key = priv_key.public_key()


    def encrypt(self, content: bytes) -> bytes:
        return rsa_encrypt_content(self.public_key, content)


    def decrypt(self, encrypted_content: bytes) -> bytes:
        return rsa_decrypt_content(self.private_key, encrypted_content)


    def serialize(self, key_type: str) -> bytes:
        match key_type:
            case "public":
                return Serialization.serialize_rsa_public_key(self.public_key)

            case "private":
                return Serialization.serialize_rsa_private_key(self.private_key)

            case _:
                raise ValueError(f"Unsupported key type: {key_type} (only 'public' or 'private')")


    @staticmethod
    def deserialize(key_type: str, content: bytes) -> RSAPrivateKey | RSAPublicKey:
        match key_type:
            case "public":
                return Serialization.deserialize_rsa_public_key(content)

            case "private":
                return Serialization.deserialize_rsa_public_key(content)

            case _:
                raise ValueError(f"Unsupported key type: {key_type} (only 'public' or 'private')")


def gen_rsa_key_pair(bit_len: int = 2048, public_exponent: int = 65537) -> dict[str, RSAPrivateKey | RSAPublicKey]:
    private_key = rsa.generate_private_key(
        key_size=bit_len,
        public_exponent=public_exponent
    )

    public_key = private_key.public_key()
    
    return {
        "public": public_key,
        "private": private_key
    }


def rsa_encrypt_content(public_key: RSAPublicKey, content: bytes) -> bytes:
    return public_key.encrypt(
        plaintext=content,
        padding=RSA_PADDING
    )


def rsa_decrypt_content(private_key: RSAPrivateKey, encrypted_content: bytes) -> bytes:
    return private_key.decrypt(
        ciphertext=encrypted_content,
        padding=RSA_PADDING
    )
