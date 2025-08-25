"""
z8ter.requests

Re-exports Starlette's Request class. Identical today, but may
gain enhancements in future Z8ter releases.
"""

from starlette.requests import Request

__all__ = [
    "Request"
]
