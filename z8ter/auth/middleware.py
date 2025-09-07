from typing import Any
from starlette.middleware.base import BaseHTTPMiddleware
from z8ter.auth.contracts import SessionRepo
from z8ter.auth.contracts import UserRepo


class AuthSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next) -> Any:
        request.state.user = None
        sid = request.cookies.get("z8_auth_sid")
        session_repo: SessionRepo = request.app.state.session_repo
        user_repo: UserRepo = request.app.state.user_repo
        if sid:
            user_id = session_repo.get_user_id(sid)
            if user_id:
                request.state.user = user_repo.get_user_by_id(user_id)
        return await call_next(request)
