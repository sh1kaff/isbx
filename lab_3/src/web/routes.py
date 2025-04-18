from aiohttp import web, ContentTypeError
from aiohttp_session import get_session
import aiohttp_jinja2
import aiofiles

from src.web.session import create_session_dir
from src.web.wrappers import (
    error_wrap,
    success_wrap,
    key_wrap,
    file_wrap
)

from src.atomic.hybrid import HybridCryptoSystem

from config.settings import gen_settings
from config.web_consts import ALLOWED_DOWNLOAD_KEYS
from config.messages import WEB_ERRORS


routes = web.RouteTableDef()


async def get_request_json_param(request: web.Request, param: str):
    try: 
        data = await request.json()
    except ContentTypeError:
        raise ContentTypeError(WEB_ERRORS["invalid_json"])

    value = data.get(param)
    if value is None:
        raise ValueError(WEB_ERRORS["required_param"].format(param))
    
    return value


@routes.get("/")
@aiohttp_jinja2.template("index.html")
async def home_handler(request: web.Request) -> dict:
    session = await get_session(request)
    return {}


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


@routes.get("/keys")
async def keys_handler(request: web.Request) -> web.Response:
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

    async with aiofiles.open(key_path, "rb") as file:
        data = await file.read()

        return file_wrap(key + ".pem", data)


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
