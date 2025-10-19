from __future__ import annotations

import asyncio
from typing import Any

from z8ter.endpoints.api import API


class SampleAPI(API):
    def __init__(self) -> None:
        super().__init__()

    calls: list[str] = []

    @API.endpoint("GET", "/hello")
    async def hello(self, request: Any):
        self.calls.append("hello")
        return {"message": "hi"}

    @API.endpoint("POST", "/echo")
    async def echo(self, request: Any):
        data = await request.json()
        return {"data": data}


def test_api_collects_and_mounts_routes() -> None:
    mount = SampleAPI.build_mount()
    assert mount.path.startswith("/")
    assert len(mount.routes) == 2

    paths = {route.path: route for route in mount.routes}
    assert "/hello" in paths
    assert "GET" in paths["/hello"].methods
    assert "/echo" in paths
    assert "POST" in paths["/echo"].methods


def test_api_endpoints_execute() -> None:
    api = SampleAPI()

    result = asyncio.run(api.hello(None))  # type: ignore[arg-type]
    assert result == {"message": "hi"}

    class Request:
        async def json(self):
            return {"value": 42}

    result = asyncio.run(api.echo(Request()))  # type: ignore[arg-type]
    assert result == {"data": {"value": 42}}
