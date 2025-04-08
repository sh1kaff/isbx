from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


HASH_ALGORITHM = hashes.SHA256()


PADDING = padding.OAEP(
    mgf=padding.MGF1(algorithm=HASH_ALGORITHM),
    algorithm=HASH_ALGORITHM,
    label=None
)
