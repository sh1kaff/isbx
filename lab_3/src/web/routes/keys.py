from aiohttp import web
from aiohttp_session import get_session

from src.atomic.rsa import RSA
from src.atomic.serialization import Serialization
from src.utils import AsyncIOUtils
from src.web.errors import valid_rsa_cast5_keys
from src.web.session import create_session_dir
from src.web.wrappers import (
    error_wrap,
    success_wrap,
    key_wrap,
    file_wrap
)

from config.settings import gen_settings
from config.web_consts import ALLOWED_DOWNLOAD_KEYS
from config.messages import WEB_ERRORS


routes = web.RouteTableDef()


@routes.get("/keys")
async def keys_get_handler(request: web.Request) -> web.Response:
    session = await get_session(request)
    session_dir = session.get("dir_path")

    if session_dir is None:
        return error_wrap(WEB_ERRORS["keys_not_yet_generated"])

    return success_wrap(
        keys=ALLOWED_DOWNLOAD_KEYS
    )


@routes.get("/keys/{key}")
async def key_get_handler(request: web.Request) -> web.Response:
    key = request.match_info.get("key", "")

    if key not in ALLOWED_DOWNLOAD_KEYS:
        return error_wrap(WEB_ERRORS["download_key_not_allowed"].format(key=key))

    session = await get_session(request)
    session_dir = session.get("dir_path")

    if session_dir is None:
        return error_wrap(WEB_ERRORS["keys_not_yet_generated"])

    key_path = key_wrap(session_dir, key)

    data = await AsyncIOUtils.async_read_bytes(key_path)
    return file_wrap(key + ".pem", data)


@routes.post("/keys")
async def keys_upload_handler(request: web.Request) -> web.Response:
    post_data = await request.post()

    rsa_file = post_data.get("rsa_private_key")
    cast5_file = post_data.get("cast5_encrypted_key")

    if any(f is None for f in (rsa_file, cast5_file)):
        return error_wrap(WEB_ERRORS["keys_required"])

    rsa_file_content = rsa_file.file.read()
    cast5_file_content = cast5_file.file.read()

    valid_rsa_cast5_keys(
        rsa_file_content,
        cast5_file_content
    )

    session = await get_session(request)
    if session.get("dir_path") is None:
        create_session_dir(session)

    settings = gen_settings(session["dir_path"])

    
    rsa_public_bytes = RSA(
        Serialization.deserialize_rsa_private_key(rsa_file_content)
        ).serialize("public")
    

    await AsyncIOUtils.async_write_bytes(
        settings["rsa_private_key"],
        rsa_file_content
    )
    await AsyncIOUtils.async_write_bytes(
        settings["rsa_public_key"],
        rsa_public_bytes
    )
    await AsyncIOUtils.async_write_bytes(
        settings["cast5_encrypted_key"],
        cast5_file_content
    )

    
    return success_wrap(keys=ALLOWED_DOWNLOAD_KEYS)
