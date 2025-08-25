from __future__ import annotations
import logging
from typing import Any, List, Optional, Sequence, cast
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount, Route
from starlette.datastructures import URLPath
from starlette.types import Receive, Scope, Send
from starlette.templating import Jinja2Templates
from z8ter import get_templates
from z8ter.route_builders import (
    build_routes_from_pages,
    build_routes_from_apis,
    build_file_routes,
)
logger = logging.getLogger("z8ter")


class Z8ter:
    def __init__(
        self,
        *,
        debug: Optional[bool] = None,
        mode: Optional[str] = None,
        routes: Optional[Sequence[Route | Mount]] = None,
        sessions: bool = False,
        session_secret: Optional[str] = None,
    ) -> None:
        self._extra_routes: List[Route | Mount] = list(routes or [])
        self.mode: str = (mode or "prod").lower()
        self.debug: bool = False
        if debug is None:
            self.debug = bool(self.mode == "dev")
        else:
            self.debug = bool(debug)
        self.app: Starlette = Starlette(debug=self.debug,
                                        routes=self._assemble_routes())

        if sessions:
            if session_secret:
                secret: str = session_secret
            else:
                raise ValueError(
                    "Z8ter: session_secret is required when sessions=True."
                )
            self.app.add_middleware(SessionMiddleware, secret_key=secret)

        def _url_for(name: str, filename: Optional[str] = None,
                     **params: Any) -> str:
            if filename is not None:
                params["path"] = filename
            path: URLPath = self.app.url_path_for(name, **params)
            return str(path)

        templates: Jinja2Templates = get_templates()
        templates.env.globals["url_for"] = _url_for

        if self.debug:
            logger.warning("🧪 Z8ter running in DEBUG mode")

    async def __call__(
            self, scope: Scope, receive: Receive, send: Send
            ) -> None:
        await self.app(scope, receive, send)

    def _assemble_routes(self) -> List[Route | Mount]:
        routes: List[Route | Mount] = []
        routes += self._extra_routes
        routes.append(build_file_routes())
        routes += build_routes_from_pages()
        routes += build_routes_from_apis()
        return routes

    def _ensure_services_registry(self) -> None:
        state: Any = self.app.state
        if not hasattr(state, "services"):
            state.services = {}

    def add_service(self, obj: object, *, replace: bool = False) -> str:
        """
        Registers a process-wide service under app.state.
        Access via:
        request.app.state.<name> or
        request.app.state.services[name]
        """
        self._ensure_services_registry()
        key: str = (obj.__class__.__name__).rstrip("_").lower()

        state: Any = self.app.state
        services: dict[str, object] = cast(dict[str, object], state.services)

        if key in services and not replace:
            raise ValueError(f"Service '{key}' already exists." +
                             "Use replace=True to overwrite.")

        services[key] = obj
        setattr(state, key, obj)
        return key
