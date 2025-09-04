from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response


class Register(View):
    async def get(self, request: Request) -> Response:
        return self.render(request, "pages/register.jinja", {})

    async def post(self):
        pass
