from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response


class Index(View):
    async def get(self, request: Request) -> Response:
        data = {"title": "Welcome to Z8ter!"}
        return self.render(request, "pages/index.jinja", data)
