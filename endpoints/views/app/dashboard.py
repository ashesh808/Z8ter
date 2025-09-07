from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response
from z8ter.auth.guards import login_required


class Dashboard(View):
    path = '/app'

    @login_required
    async def get(self, request: Request) -> Response:
        check_dashboard: list = list(
            request.session.get("check_dashboard", [])
        )
        counter = check_dashboard[-1] if len(check_dashboard) > 0 else 0
        counter += 1
        check_dashboard.append(counter)
        request.session["draft_ids"] = list(check_dashboard)
        return self.render(request, "pages/app/dashboard.jinja", {})
