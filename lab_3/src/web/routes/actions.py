from aiohttp import web
from aiohttp_session import get_session

from src.web.session import create_session_dir
from src.web.wrappers import (
    error_wrap,
    success_wrap,
    file_wrap
)

from src.atomic.hybrid import HybridCryptoSystem

from config.settings import gen_settings
from config.web_consts import ALLOWED_DOWNLOAD_KEYS
from config.messages import WEB_ERRORS


routes = web.RouteTableDef()


@routes.post("/generate")
async def generate_handler(request: web.Request) -> web.Response:
    data = await request.json()

    session = await get_session(request)

    if session.get("dir_path") is None:
        create_session_dir(session)

    settings = gen_settings(session["dir_path"])

    hybrid = HybridCryptoSystem(cast5_keylen=data.get("cast5_keylen", 128))
    hybrid.serialize_keys_to_files(
        settings["rsa_private_key"],
        settings["rsa_public_key"],
        settings["cast5_encrypted_key"]
    )

    return success_wrap(keys=ALLOWED_DOWNLOAD_KEYS)


@routes.post("/{action:(encrypt|decrypt)}")
async def encrypt_decrypt_handler(request: web.Request) -> web.Response:
    post_data = await request.post()
    file = post_data.get("file")

    if file is None:
        return error_wrap(WEB_ERRORS["no_file_key"])

    session = await get_session(request)
    session_dir = session.get("dir_path")

    if session_dir is None:
        return error_wrap(WEB_ERRORS["keys_not_yet_generated"])

    settings = gen_settings(session["dir_path"])

    hybrid = HybridCryptoSystem()
    hybrid.import_keys_from_files(
        settings["rsa_private_key"],
        settings["cast5_encrypted_key"]
    )

    action = request.match_info["action"]
    data = file.file.read()
    match action:
        case "encrypt":
            response_data = hybrid.encrypt_content(data)
        case "decrypt":
            response_data = hybrid.decrypt_content(data)

    return file_wrap(
        file.filename,
        response_data
    )
