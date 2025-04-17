from aiohttp import web
import os


def key_wrap(base_dir: str, key: str, ext: str = ".pem") -> str:
    return os.path.join(
        base_dir,
        key + ext
    )


def file_wrap(filename: str, data: bytes) -> web.Response:
    return web.Response(
        body=data,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


def success_wrap(text: str, **kwargs) -> web.Response:
    return web.json_response({
        "success": text,
        **kwargs
    })


def error_wrap(text: str) -> web.Response:
    return web.json_response({
        "error": text
    })
