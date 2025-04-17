from aiohttp_session import setup, Session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp.web import Application

from cryptography import fernet
import secrets
import shutil
import os

from config.web_consts import WEB_ERRORS
from config.paths import TMP_DIR


async def cleanup_tmp(app: Application):
    tmp_dir = app["tmp_dir"]
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    yield

    shutil.rmtree(tmp_dir, ignore_errors=True)


def create_session_dir(session: Session):
    dir_name = secrets.token_hex(32)

    if session.get("dir_path") is not None:
        raise ValueError(WEB_ERRORS["session_dir_already_created"])

    session_dir = os.path.join(
        TMP_DIR,
        dir_name
    )

    os.makedirs(session_dir)
    session["dir_path"] = session_dir


def create_session_key() -> fernet.Fernet:
    fernet_key = fernet.Fernet.generate_key()
    
    return fernet.Fernet(fernet_key)


def setup_session(app: Application):
    session_key = create_session_key()

    setup(
        app=app,
        storage=EncryptedCookieStorage(session_key)
    )
