from aiohttp import web
import aiohttp_jinja2
import jinja2

from src.web.routes import routes
from src.web.session import setup_session, cleanup_tmp

from config.paths import(
    TEMPLATES_DIR,
    STATIC_DIR,
    TMP_DIR
)


async def init_app() -> web.Application:
    app = web.Application()

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(TEMPLATES_DIR)
    )
    
    app.add_routes(routes)

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
