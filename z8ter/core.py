from __future__ import annotations
from pathlib import Path
import os
import logging
from starlette.applications import Starlette
from starlette.routing import Route
import uvicorn
from z8ter.router import catch_all_route, build_routes_from_views
logger = logging.getLogger("z8ter")


class Z8ter:
    def __init__(
        self,
        *,
        debug: bool | None = None,
        mode: str | None = None,
        views_dir: str | Path = "views",
    ) -> None:
        env_mode = (os.getenv("Z8_MODE") or "").strip().lower() or None
        self.mode = (mode or env_mode or "prod").lower()
        self.debug = bool(self.mode == "dev") if debug is None else bool(debug)
        self.views_dir = Path(views_dir).resolve()
        if self.debug:
            logger.warning("🚀 Z8ter running in DEV mode")
            routes: list[Route] = catch_all_route(
                views_dir=str(self.views_dir))
        else:
            logger.info("🚀 Z8ter running in PROD mode")
            routes = build_routes_from_views(views_dir=str(self.views_dir))
        self.app = Starlette(debug=self.debug, routes=routes)

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)

    def run(
        self,
        host: str = "127.0.0.1",
        port: int = 8000,
        reload: bool | None = None,
    ) -> None:
        reload = self.debug if reload is None else reload
        uvicorn.run(self, host=host, port=port, reload=reload)
