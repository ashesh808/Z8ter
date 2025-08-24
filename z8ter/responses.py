"""
z8ter.responses

Re-exports Starlette’s response classes. Identical today, but may
gain enhancements in future Z8ter releases.
"""

from starlette.responses import (
    Response,
    JSONResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    FileResponse,
    StreamingResponse,
)

__all__ = [
    "Response",
    "JSONResponse",
    "HTMLResponse",
    "PlainTextResponse",
    "RedirectResponse",
    "FileResponse",
    "StreamingResponse",
]
