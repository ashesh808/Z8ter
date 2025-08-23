from __future__ import annotations
from pathlib import Path
import logging
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware.sessions import SessionMiddleware
from typing import List
import uvicorn
from starlette.staticfiles import StaticFiles
from z8ter import templates
from z8ter.router import build_routes_from_pages, build_routes_from_apis
logger = logging.getLogger("z8ter")


class Z8ter:
    def __init__(
        self,
        *,
        debug: bool | None = None,
        mode: str | None = None,
        views_dir: str | Path = "views",
        routes: list | None = None,
        sessions: bool = False,
        session_secret: str | None = None,
    ) -> None:
        self._extra_routes: list = list(routes or [])
        self.mode = (mode or "prod").lower()
        self.debug = bool(self.mode == "dev") if debug is None else bool(debug)
        self.views_dir = Path(views_dir).resolve()
        self.app = Starlette(debug=self.debug, routes=self._assemble_routes())
        if sessions:
            if session_secret:
                secret = session_secret
            else:
                raise ValueError(
                    "Z8ter: session_secret is required when sessions=True."
                )
            self.app.add_middleware(SessionMiddleware, secret_key=secret)
        static_dir = Path("static")
        if static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_dir)),
                           name="static")

        def _url_for(name: str, filename: str | None = None, **params):
            if filename is not None:
                params["path"] = filename
            return self.app.url_path_for(name, **params)

        templates.env.globals["url_for"] = _url_for

    def _assemble_routes(self) -> List[Route]:
        routes = []
        routes += self._extra_routes
        if self.debug:
            logger.warning("🚀 Z8ter running in DEV mode")
        else:
            logger.info("🚀 Z8ter running in PROD mode")
        routes += build_routes_from_pages()
        routes += build_routes_from_apis()
        return routes

    def _ensure_services_registry(self) -> None:
        if not hasattr(self.app.state, "services"):
            self.app.state.services = {}

    def add_service(
            self, obj: object, *,
            replace: bool = False
            ) -> str:
        """
        Registers a process-wide service under app.state.
        Access via: request.app.state.<name> or
        request.app.state.services[name]
        """
        self._ensure_services_registry()
        key = (obj.__class__.__name__).rstrip("_").lower()

        if key in self.app.state.services and not replace:
            raise ValueError(
                f"Service '{key}' already exists." +
                "Use replace=True to overwrite."
            )
        self.app.state.services[key] = obj
        setattr(self.app.state, key, obj)
        return key

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)

    def run(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        reload: bool | None = None,
    ) -> None:
        reload = self.debug if reload is None else reload
        uvicorn.run(
            "main:app" if reload else self,
            host=host,
            port=port,
            reload=reload
        )
