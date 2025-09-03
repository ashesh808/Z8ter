from __future__ import annotations
from typing import Any, ClassVar, Optional
from starlette.endpoints import HTTPEndpoint
from starlette.types import Receive, Scope, Send
from z8ter.requests import Request
from z8ter.responses import Response
from z8ter.endpoints.helpers import render, load_content


class View(HTTPEndpoint):
    """HTTPEndpoint + a small render() helper for templates."""

    _page_id: ClassVar[str]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        mod: str = cls.__module__
        if mod.startswith("endpoints.views."):
            pid = mod.removeprefix("endpoints.views.")
        else:
            pid = mod
        cls._page_id = pid

    def __init__(
        self,
        scope: Optional[Scope] = None,
        receive: Optional[Receive] = None,
        send: Optional[Send] = None,
    ) -> None:
        if scope is not None and receive is not None and send is not None:
            super().__init__(scope, receive, send)

    def render(
        self,
        request: Request,
        template_name: str,
        context: dict[str, Any] | None = None,
    ) -> Response:
        page_id: str = getattr(self.__class__, "_page_id", "")
        ctx: dict[str, Any] = {"page_id": page_id, "request": request}
        if context:
            ctx.update(context)
        ctx.update(load_content(page_id))
        return render(template_name, ctx)
