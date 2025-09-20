"""Z8ter request class.

Re-exports Starlette's `Request` so applications can consistently
import from `z8ter.requests`.

This creates a stable abstraction layer where Z8ter may later:
  - Add convenience methods (e.g., session/user helpers).
  - Enforce framework-wide conventions (e.g., typed state).
  - Swap out the base request implementation if needed.

Currently, this is identical to Starlette's `Request`.
"""

from starlette.requests import Request

__all__ = ["Request"]
