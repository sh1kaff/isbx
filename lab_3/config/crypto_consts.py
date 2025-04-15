from cryptography.hazmat.primitives import padding
import cryptography.hazmat.primitives.asymmetric.padding as asymm_padding
from cryptography.hazmat.primitives import hashes


CAST5_ENCRYPTED_TITLE = "CAST5 ENCRYPTED KEY"


CAST5_PADDING = padding.PKCS7(128)


RSA_HASH_ALGORITHM = hashes.SHA256()


RSA_PADDING = asymm_padding.OAEP(
    mgf=asymm_padding.MGF1(algorithm=RSA_HASH_ALGORITHM),
    algorithm=RSA_HASH_ALGORITHM,
    label=None
)
