"""Base class for SSR views.

`View` extends Starlette's `HTTPEndpoint` and adds a convenience `render()`
method that:
  - Injects `request` and a stable `page_id` into the template context.
  - Loads page-scoped YAML content via `load_content(page_id)` and merges it.

`page_id` derivation:
- If the subclass lives under `endpoints.views.<pkg>.<module>`, the prefix
  `endpoints.views.` is stripped. Otherwise, the full module path is used.
- The resulting dot-path (e.g., "about" or "app.home") is exposed as `page_id`.
"""

from __future__ import annotations

from typing import Any, ClassVar

from starlette.endpoints import HTTPEndpoint
from starlette.types import Receive, Scope, Send

# NOTE: The module is named "helpers.py", not "helper.py".
from z8ter.endpoints.helpers import load_content, render
from z8ter.requests import Request
from z8ter.responses import Response


class View(HTTPEndpoint):
    """HTTPEndpoint with a small `render()` helper for templates.

    Class Attributes:
        _page_id: Stable identifier derived from the module path. Used by the
            templating layer and client-side "islands" contract.
    """

    _page_id: ClassVar[str]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Derive and cache a stable `page_id` for the subclass.

        Rules:
            - If module starts with "endpoints.views.", strip that prefix.
            - Otherwise, use the module path as-is.

        The value is a dot-separated string (e.g., "about", "app.home").
        """
        super().__init_subclass__(**kwargs)
        mod: str = cls.__module__
        if mod.startswith("endpoints.views."):
            pid = mod.removeprefix("endpoints.views.")
        else:
            pid = mod
        cls._page_id = pid

    def __init__(
        self,
        scope: Scope | None = None,
        receive: Receive | None = None,
        send: Send | None = None,
    ) -> None:
        """Support manual instantiation in tests.

        Starlette constructs endpoint instances with `(scope, receive, send)`.
        This initializer calls the parent only when all three are provided.
        """
        if scope is not None and receive is not None and send is not None:
            super().__init__(scope, receive, send)

    def render(
        self,
        request: Request,
        template_name: str,
        context: dict[str, Any] | None = None,
    ) -> Response:
        """Render a template with standard SSR context.

        Injects:
            - `page_id`: Derived from the subclass module path.
            - `request`: The current request object (for Jinja/Starlette usage).
            - `page_content`: YAML loaded via `load_content(page_id)`.

        Args:
            request: Current HTTP request.
            template_name: Template path relative to the templates directory.
            context: Additional context values to merge (optional).

        Returns:
            Response: Starlette `TemplateResponse`.

        Notes:
            - `load_content` expects a YAML file at `content/{page_id}.yaml`
              (dots in `page_id` become slashes). Exceptions from missing or
              malformed content will propagate unless handled by the caller.

        """
        page_id: str = getattr(self.__class__, "_page_id", "")
        ctx: dict[str, Any] = {"page_id": page_id, "request": request}
        if context:
            ctx.update(context)
        ctx.update(load_content(page_id))
        return render(template_name, ctx)
