import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.decrepit.ciphers.algorithms import CAST5
from cryptography.hazmat.primitives import padding

from cryptography.hazmat.primitives.asymmetric import rsa, padding

# https://elc.github.io/python-security/chapters/06_Symmetric_Encryption.html

key = secrets.token_bytes(5)
iv = secrets.token_bytes(8)

cipher = Cipher(
    CAST5(key),
    modes.CBC(iv)
)

encryptor = cipher.encryptor()
# padder = padding.PKCS7(128).padder()

data = b"Hey my boy#$%^&*"
# padded_data = padder.update(data) + padder.finalize()

ciphertext = encryptor.update(data) + encryptor.finalize()

print(ciphertext)

decryptor = cipher.decryptor()
# unpadder = padding.PKCS7(128).unpadder()

decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
# unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

print(decrypted_data)