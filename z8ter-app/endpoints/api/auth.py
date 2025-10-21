from z8ter.responses import RedirectResponse
from z8ter.requests import Request
from z8ter.endpoints.api import API
from app.identity.usecases.manage_sessions import ManageSessions


class Auth(API):
    def __init__(self) -> None:
        super().__init__()

    @API.endpoint("POST", "/logout")
    async def send_hello(self, request: Request) -> RedirectResponse:
        ms = ManageSessions(request.app.state.session_repo)
        sid = request.cookies.get("z8_sid")
        if sid:
            await ms.revoke_session(sid)
        resp = RedirectResponse("/login?m=logged_out", status_code=303)
        await ms.clear_session_cookie(resp)
        return resp
