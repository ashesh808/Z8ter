from z8ter.api import API
from starlette.responses import JSONResponse
from starlette.requests import Request


class Hello(API):
    def __init__(self) -> None:
        super().__init__()

    @API.endpoint("GET", "/")
    async def send_hello(self, request: Request) -> JSONResponse:
        content = {"message": "Hello from the API!"}
        return JSONResponse(content, 200)
