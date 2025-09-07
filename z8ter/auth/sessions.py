import secrets
from datetime import datetime, timedelta, timezone
from z8ter.responses import Response
from z8ter.auth.contracts import SessionRepo


class SessionManager:
    def __init__(self, session_repo: SessionRepo):
        self.cookie_name = "z8_sid"
        self.session_repo = session_repo

    async def start_session(
        self,
        user_id: str,
        *,
        remember: bool = False,
        ip: str | None = None,
        user_agent: str | None = None,
        ttl: int = 60 * 60 * 24 * 7,
    ) -> str:
        sid = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)
        self.session_repo.insert(
            sid_plain=sid,
            user_id=user_id,
            expires_at=expires_at,
            remember=remember,
            ip=ip,
            user_agent=user_agent,
        )
        return sid

    async def revoke_session(self, sid: str) -> bool:
        return self.session_repo.revoke(sid_plain=sid)

    async def set_session_cookie(
        self,
        resp: Response,
        sid: str,
        *,
        secure: bool = True,
        remember: bool = False,
        ttl: int = 60 * 60 * 24 * 7,
    ) -> None:
        max_age = ttl if remember else None
        resp.set_cookie(
            key=self.cookie_name,
            value=sid,
            httponly=True,
            secure=secure,
            samesite="lax",
            path="/",
            max_age=max_age,
        )

    async def clear_session_cookie(self, resp: Response) -> None:
        resp.delete_cookie(self.cookie_name, path="/")
