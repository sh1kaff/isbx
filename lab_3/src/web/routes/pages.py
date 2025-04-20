from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2


routes = web.RouteTableDef()


@routes.get("/")
@aiohttp_jinja2.template("index.html")
async def home_handler(request: web.Request) -> dict:
    """Index page"""
    session = await get_session(request)
    return {}
