from __future__ import annotations
import logging
from typing import Optional
from starlette.applications import Starlette
from starlette.types import Receive, Scope, Send

logger = logging.getLogger("z8ter")


class Z8ter:
    def __init__(
        self,
        *,
        debug: Optional[bool] = None,
        mode: Optional[str] = None,
        starlette_app: Starlette
    ) -> None:
        self.starlette_app = starlette_app
        self.state = starlette_app.state
        self.mode: str = (mode or "prod").lower()
        self.debug: bool = False
        if debug is None:
            self.debug = bool(self.mode == "dev")
        else:
            self.debug = bool(debug)
        if self.debug:
            logger.warning("🧪 Z8ter running in DEBUG mode")

    async def __call__(
            self, scope: Scope, receive: Receive, send: Send
            ) -> None:
        await self.starlette_app(scope, receive, send)
