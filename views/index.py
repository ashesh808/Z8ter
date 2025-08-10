from z8ter.page import Page
from starlette.requests import Request
from starlette.responses import Response


class Index(Page):
    async def get(self, request: Request) -> Response:
        data = {"title": "Welcome to Z8ter!"}
        return self.render(request, "index.jinja", data)
