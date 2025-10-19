from __future__ import annotations

from starlette.requests import Request as StarletteRequest

from z8ter.requests import Request


def test_request_is_starlette_request() -> None:
    assert Request is StarletteRequest
