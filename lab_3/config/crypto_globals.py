from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


CAST5_ENCRYPTED_SERIALIZATION_HEADERS = {
    "start": b"-----BEGIN CAST5 ENCRYPTED KEY-----\n",
    "end": b"-----END CAST5 ENCRYPTED KEY-----\n"
}


HASH_ALGORITHM = hashes.SHA256()


PADDING = padding.OAEP(
    mgf=padding.MGF1(algorithm=HASH_ALGORITHM),
    algorithm=HASH_ALGORITHM,
    label=None
)
