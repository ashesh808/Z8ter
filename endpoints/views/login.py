from starlette.datastructures import FormData
from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response, RedirectResponse
from z8ter.auth.crypto import verify_password
from app.identity.usecases.manage_sessions import (
    start_session, set_session_cookie
)
from app.identity.usecases.manage_users import (
    get_user_email
)


class Login(View):
    async def get(self, request: Request) -> Response:
        return self.render(request, "pages/login.jinja", {})

    async def post(self, request: Request) -> Response:
        form: FormData = await request.form()
        if form is None:
            raise TypeError("Form data is None")
        email = str(form.get("email") or "").strip()
        pwd = str(form.get("password") or "")
        user = get_user_email(email)
        if user is None:
            return RedirectResponse(
                "/login?e=badcreds", status_code=303
            )
        ok = verify_password(user["password_hash"], pwd)
        if not ok:
            return RedirectResponse("/login?e=badcreds", status_code=303)
        sid = start_session(user["id"])
        resp = RedirectResponse("/app", status_code=303)
        set_session_cookie(resp, sid, secure=False)
        return resp
