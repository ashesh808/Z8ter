"""Z8ter core application wrapper.

Provides the `Z8ter` class, which wraps a Starlette application and
adds framework-specific state, debug handling, and logging.
"""

from __future__ import annotations

import logging

from starlette.applications import Starlette
from starlette.types import Receive, Scope, Send

logger = logging.getLogger("z8ter")


class Z8ter:
    """Z8ter application wrapper around Starlette.

    This class holds a reference to the underlying Starlette app, exposes
    its state, and manages framework-level debug/mode settings.

    Args:
        debug: Optional explicit debug flag. If None, defaults to True
            when mode="dev".
        mode: Application mode string (e.g., "dev", "prod"). Defaults
            to "prod" if not set.
        starlette_app: The underlying Starlette ASGI application.

    Attributes:
        starlette_app: The wrapped Starlette application instance.
        state: Shortcut to `starlette_app.state`.
        mode: Lowercased mode string (default "prod").
        debug: Boolean indicating whether debug mode is active.

    Notes:
        - In debug mode, a warning banner is logged at startup.
        - The class is itself ASGI-callable (`__call__` forwards to
          `starlette_app`).

    """

    def __init__(
        self,
        *,
        debug: bool | None = None,
        mode: str | None = None,
        starlette_app: Starlette,
    ) -> None:
        """Initialize Z8ter apps, this should only be done via the App builder."""
        self.starlette_app = starlette_app
        self.state = starlette_app.state
        self.mode: str = (mode or "prod").lower()
        if debug is None:
            self.debug = self.mode == "dev"
        else:
            self.debug = bool(debug)
        if self.debug:
            logger.warning("🧪 Z8ter running in DEBUG mode")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Forward ASGI calls directly to the underlying Starlette app.

        Args:
            scope: The ASGI connection scope.
            receive: Awaitable to receive ASGI events.
            send: Awaitable to send ASGI events.

        Returns:
            None. The ASGI response cycle is handled by Starlette.

        """
        await self.starlette_app(scope, receive, send)
