from starlette.datastructures import FormData
from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response, RedirectResponse
from z8ter.auth.crypto import verify_password
from z8ter.auth.guards import skip_if_authenticated
from app.identity.usecases.manage_sessions import ManageSessions
from app.identity.usecases.manage_users import ManageUsers


class Login(View):
    @skip_if_authenticated
    async def get(self, request: Request) -> Response:
        return self.render(request, "pages/login.jinja", {})

    @skip_if_authenticated
    async def post(self, request: Request) -> Response:
        form: FormData = await request.form()
        ms = ManageSessions(request.app.state.session_repo)
        mu = ManageUsers(request.app.state.user_repo)
        if form is None:
            raise TypeError("Form data is None")
        email = str(form.get("email") or "").strip()
        pwd = str(form.get("password") or "")
        user = await mu.get_user_email(email)
        if user is None:
            return RedirectResponse(
                "/login?e=badcreds", status_code=303
            )
        ok = verify_password(user["pwd_hash"], pwd)
        if not ok:
            return RedirectResponse("/login?e=badcreds", status_code=303)
        sid = await ms.start_session(user["id"])
        resp = RedirectResponse("/app", status_code=303)
        await ms.set_session_cookie(resp, sid, secure=False)
        return resp
