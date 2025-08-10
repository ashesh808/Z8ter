from z8ter.page import Page
from starlette.requests import Request
from starlette.responses import Response


class About(Page):
    async def get(self, request: Request) -> Response:
        return self.render(request, "about.jinja", {})
