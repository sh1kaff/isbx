from aiohttp import web
import aiohttp_jinja2
import jinja2

from src.web.errors import error_middleware
from src.web.routes import actions, keys, pages
from src.web.session import setup_session, cleanup_tmp

from config.paths import(
    TEMPLATES_DIR,
    STATIC_DIR,
    TMP_DIR
)
from config.web_consts import ALLOWED_DOWNLOAD_KEYS


async def init_app() -> web.Application:
    """Initializes the web application

    Returns:
        web.Application: Web Application
    """
    app = web.Application(
        middlewares=[error_middleware]
    )

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR)
    ).globals.update(
        ALLOWED_DOWNLOAD_KEYS=ALLOWED_DOWNLOAD_KEYS
    )

    app.add_routes([
        *actions.routes,
        *keys.routes,
        *pages.routes
    ])

    app.router.add_static(
        prefix="/static/",
        path=STATIC_DIR,
        name="static"
    )

    app["tmp_dir"] = TMP_DIR
    setup_session(app)
    app.cleanup_ctx.append(cleanup_tmp)

    return app


if __name__ == "__main__":
    web.run_app(init_app())
