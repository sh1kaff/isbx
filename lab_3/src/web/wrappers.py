from aiohttp import web
import os


def key_wrap(base_dir: str, key: str, ext: str = ".pem") -> str:
    """Wrapper for key"""
    return os.path.join(
        base_dir,
        key + ext
    )


def status_wrap(status_key: str, status: int = 200, **kwargs) -> web.Response:
    """Status wrapper"""
    return web.json_response({
        "status": status_key,
        **kwargs
    }, status=status)


def file_wrap(filename: str, data: bytes) -> web.Response:
    """File wrapper"""
    return web.Response(
        body=data,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


def success_wrap(**kwargs) -> web.Response:
    """Success wrapper"""
    return status_wrap(
        "success",
        **kwargs
    )


def error_wrap(text: str, **kwargs) -> web.Response:
    """Error wrapper"""
    return status_wrap(
        "error",
        message=text,
        status=500,
        **kwargs
    )
