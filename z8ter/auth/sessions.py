import secrets
from datetime import datetime
from z8ter.responses import Response
from z8ter.db.session_repo import SessionRepo


class SessionManager:
    def __init__(self, cookie_name: str, session_repo: SessionRepo):
        self.cookie_name = cookie_name
        self.session_repo = session_repo

    async def start_session(self, user_id):
        sid = secrets.token_urlsafe(32)
        self.session_repo.insert(
            sid_plain=sid,
            user_id=user_id,
            expires_at=datetime.now(),
            remember=False,
            ip="12314",
            user_agent="sfssf"
        )
        return sid

    async def revoke_session(self, sid):
        self.session_repo.revoke(sid_plain=sid)

    async def set_session_cookie(
            self, resp: Response, sid: str, *, secure: bool
    ):
        resp.set_cookie(
            key=self.cookie_name,
            value=sid,
            httponly=True,
            secure=secure,
            samesite="lax",
            path="/",
            max_age=60*60*24*7
        )

    async def clear_session_cookie(self, resp: Response):
        resp.delete_cookie(self.cookie_name, path="/")
