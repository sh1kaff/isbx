from secrets import token_bytes
from cryptography.hazmat.primitives.asymmetric import rsa


def gen_cast5_key(bit_len: int) -> bytes:
    if bit_len < 40 or bit_len > 128:
        raise ValueError("The key length must be between 40 and 128 bits inclusive")

    if bit_len % 8 != 0:
        raise ValueError("The key length should be in 8 bit increments")
    
    return token_bytes(bit_len * 8)


def gen_rsa_key_pair(bit_len: int = 2048, public_exponent: int = 65537) -> dict:
    private_key = rsa.generate_private_key(
        key_size=bit_len,
        public_exponent=public_exponent
    )

    public_key = private_key.public_key()
    
    return {
        "public": public_key,
        "private": private_key
    }
