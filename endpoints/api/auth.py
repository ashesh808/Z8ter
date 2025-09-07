from z8ter.responses import RedirectResponse
from z8ter.requests import Request
from z8ter.endpoints.api import API
from app.identity.usecases.manage_sessions import (
    revoke_session, clear_session_cookie
)


class Auth(API):
    def __init__(self) -> None:
        super().__init__()

    @API.endpoint("POST", "/logout")
    async def send_hello(self, request: Request) -> RedirectResponse:
        sid = request.cookies.get("z8_sid")
        if sid:
            revoke_session(sid)
        resp = RedirectResponse("/login?m=logged_out", status_code=303)
        clear_session_cookie(resp)
        return resp
