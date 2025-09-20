from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response


class About(View):
    async def get(self, request: Request) -> Response:
        return self.render(request, "pages/about.jinja", {})
