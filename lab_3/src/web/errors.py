from aiohttp import web
from src.web.wrappers import error_wrap


@web.middleware
async def error_middleware(request: web.Request, handler) -> web.Response:
    try:
        response = await handler(request)
        return response
    except Exception as e:
        return error_wrap(str(e))
