from __future__ import annotations
from starlette.requests import Request
from starlette.responses import Response
from starlette.endpoints import HTTPEndpoint
from z8ter import templates


class Page(HTTPEndpoint):
    """HTTPEndpoint + a small render() helper for templates."""
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        mod = cls.__module__
        if mod.startswith("views."):
            pid = mod.removeprefix("views.")
        else:
            pid = mod
        cls._page_id = pid

    def __init__(self, scope=None, receive=None, send=None):
        if scope is not None and receive is not None and send is not None:
            super().__init__(scope, receive, send)

    def render(self, request: Request, template_name: str,
               context: dict | None = None) -> Response:
        page_id = getattr(self.__class__, "_page_id", None)
        ctx = {"page_id": page_id, "request": request}
        if context:
            ctx.update(context)
        return templates.TemplateResponse(template_name, ctx)
