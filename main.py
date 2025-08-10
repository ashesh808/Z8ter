import logging
from z8ter.core import Z8ter
from starlette.routing import Route
from starlette.responses import FileResponse
from config import FAVICON_PATH, VIEW_PATH
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


async def favicon(_):
    return FileResponse(FAVICON_PATH)

app = Z8ter(routes=[Route("/favicon.ico", favicon, methods=["GET"])],
            views_dir=VIEW_PATH)

if __name__ == "__main__":
    app.run()
