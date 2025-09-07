from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response
from z8ter.auth.guards import login_required


class Dashboard(View):
    path = '/app'

    @login_required
    async def get(self, request: Request) -> Response:
        return self.render(request, "pages/app/dashboard.jinja", {})
