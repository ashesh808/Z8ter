from z8ter.endpoints.view import View
from z8ter.requests import Request
from z8ter.responses import Response, RedirectResponse
from app.identity.usecases.manage_users import ManageUsers


class Register(View):
    async def get(self, request: Request) -> Response:
        return self.render(request, "pages/register.jinja", {})

    async def post(self, request: Request) -> Response:
        mu = ManageUsers(request.app.state.user_repo)
        form = await request.form()
        email = str(form.get("email") or "").strip().lower()
        pwd = str(form.get("password") or "")
        pwd2 = str(form.get("password2") or "")
        if (not email) or (not pwd) or (pwd != pwd2):
            return RedirectResponse("/register?e=invalid", status_code=303)
        await mu.create_user(email, pwd)
        return RedirectResponse("/login?m=signup_ok", status_code=303)
