from __future__ import annotations
from pathlib import Path
import logging
from starlette.applications import Starlette
from starlette.routing import Route
from typing import List
import uvicorn
from config import Z8_MODE
from z8ter.router import build_routes_from_pages
logger = logging.getLogger("z8ter")


class Z8ter:
    def __init__(
        self,
        *,
        debug: bool | None = None,
        mode: str | None = None,
        views_dir: str | Path = "views",
        routes: list | None = None
    ) -> None:
        self._extra_routes: list = list(routes or [])
        env_mode = (Z8_MODE or "").strip().lower() or None
        self.mode = (mode or env_mode or "prod").lower()
        self.debug = bool(self.mode == "dev") if debug is None else bool(debug)
        self.views_dir = Path(views_dir).resolve()
        self.app = Starlette(debug=self.debug, routes=self._assemble_routes())

    def _assemble_routes(self) -> List[Route]:
        routes = []
        routes += self._extra_routes
        if self.debug:
            logger.warning("🚀 Z8ter running in DEV mode")
        else:
            logger.info("🚀 Z8ter running in PROD mode")
        routes += build_routes_from_pages(pages_dir=str(self.views_dir))
        return routes

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)

    def run(
        self,
        host: str = "127.0.0.1",
        port: int = 8000,
        reload: bool | None = None,
    ) -> None:
        reload = self.debug if reload is None else reload
        uvicorn.run(
            "main:app" if reload else self,
            host=host,
            port=port,
            reload=reload
        )
