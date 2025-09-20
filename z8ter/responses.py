"""Z8ter response classes.

This module re-exports Starlette's core `Response` classes so that
applications can import from `z8ter.responses` instead of depending
on Starlette directly. This creates a stable abstraction layer where
Z8ter can later:
  - Add defaults (e.g., headers, encoding).
  - Provide custom response subclasses.
  - Swap implementations without breaking app code.

Today these are identical to Starlette's responses.
"""

from starlette.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
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
