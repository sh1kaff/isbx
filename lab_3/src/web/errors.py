from aiohttp import web
from src.web.wrappers import error_wrap

from src.atomic.serialization import Serialization
from src.atomic.hybrid import rsa_decrypt_cast5_key

from config.messages import WEB_ERRORS
from config.web_consts import MAX_UPLOADED_SIZE


@web.middleware
async def error_middleware(request: web.Request, handler) -> web.Response:
    try:
        response = await handler(request)
        return response
    except Exception as e:
        return error_wrap(str(e))


def valid_rsa_cast5_keys(rsa_key_ser: bytes, cast5_key_ser: bytes):
    try:
        rsa_private_key = Serialization.deserialize_rsa_private_key(rsa_key_ser)
        cast5_encrypted_key = Serialization.deserialize_cast5_encrypted_key(cast5_key_ser)
        
        rsa_decrypt_cast5_key(
            rsa_private_key,
            cast5_encrypted_key
        )
    except:
        raise ValueError(WEB_ERRORS["invalid_key_pair"])


def valid_file_size(file):
    if len(file.file.read()) > MAX_UPLOADED_SIZE:
        raise ValueError(WEB_ERRORS["max_size"].format(size=MAX_UPLOADED_SIZE))

    file.file.seek(0)
