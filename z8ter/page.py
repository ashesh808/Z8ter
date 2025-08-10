from __future__ import annotations
from abc import ABC, abstractmethod
from starlette.requests import Request
from starlette.responses import Response
from z8ter import templates


class Page(ABC):
    """
    Base contract for Z8ter pages.

    Routing:
      - Router discovers subclasses of Page in views/pages/*
      - Route path is inferred from file path unless `path` is set explicitly.

    Rendering:
      - Concrete pages implement `get()` (and optionally `post()`),
        returning a Starlette Response.
      - Use `render_file()` for now to return static HTML; swap to Jinja later.
    """

    # Override to force a custom URL (e.g., "/")
    path: str | None = None

    @abstractmethod
    async def get(self, request: Request) -> Response:
        """Handle GET. Must return a Response."""
        raise NotImplementedError

    async def post(self, request: Request) -> Response:
        """Handle POST. Default is 405 until a page opts in."""
        return Response(status_code=405)

    def render(
            self, request: Request, template_name: str, context: dict
          ) -> Response:
        context = context or {}
        context.update({"request": request})
        return templates.TemplateResponse(template_name, context)
