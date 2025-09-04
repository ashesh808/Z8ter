from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response, RedirectResponse
from z8ter.db import get_conn
from z8ter.auth.repo import get_user_email
from z8ter.auth.crypto import verify_password
from starlette.datastructures import FormData


class Login(View):
    async def get(self, request: Request) -> Response:
        return self.render(request, "pages/login.jinja", {})

    async def post(self, request: Request) -> Response:
        form: FormData = await request.form()
        if form is None:
            raise TypeError("Form data is None")
        email = str(form.get("email") or "").strip()
        pwd = str(form.get("password") or "")
        conn = get_conn()
        user = get_user_email(conn, email)
        if user is None:
            return RedirectResponse(
                "/login?e=badcreds", status_code=303
            )
        ok = verify_password(user["password_hash"], pwd)
        return RedirectResponse(
            "/" if ok else "/login?e=badcreds", status_code=303
        )
