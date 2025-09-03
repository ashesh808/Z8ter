from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response

class Register(View):
    async def get(self, request: Request) -> Response:
        # Load your YAML separately and pass as "page_content" in context if desired
        return self.render(request, "pages/register.jinja", {})