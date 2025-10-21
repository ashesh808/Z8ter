from z8ter.auth.sessions import SessionManager
from z8ter.responses import Response


class ManageSessions:
    def __init__(self, session_repo) -> None:
        self.session_repo = session_repo
        self.session_manager = SessionManager(session_repo=session_repo)

    async def start_session(self, uid: str) -> str:
        """Create a session and return the new sid."""
        sid = await self.session_manager.start_session(user_id=uid)
        return sid

    async def revoke_session(self, sid: str) -> bool:
        """Revoke a session."""
        return await self.session_manager.revoke_session(sid)

    async def set_session_cookie(
        self, resp: Response, sid: str, secure: bool = True
    ) -> None:
        """Attach session cookie to response."""
        await self.session_manager.set_session_cookie(resp, sid, secure=secure)

    async def clear_session_cookie(self, resp: Response) -> None:
        """Remove session cookie from response."""
        await self.session_manager.clear_session_cookie(resp)
