from __future__ import annotations
from typing import Optional
from datetime import datetime, timezone


class InMemorySessionRepo:
    def __init__(self) -> None:
        self._sessions: dict[str, dict] = {}

    def insert(
        self,
        *,
        sid_plain: str,
        user_id: str,
        expires_at: datetime,
        remember: bool,
        ip: Optional[str],
        user_agent: Optional[str],
        rotated_from_sid: Optional[str] = None,
    ) -> None:
        self._sessions[sid_plain] = {
            "user_id": user_id,
            "expires_at": expires_at,
            "remember": remember,
            "ip": ip,
            "user_agent": user_agent,
            "revoked_at": None,
            "rotated_from_sid": rotated_from_sid,
        }

    def revoke(self, *, sid_plain: str) -> bool:
        session = self._sessions.get(sid_plain)
        if not session:
            return False
        if session["revoked_at"] is not None:
            return False
        session["revoked_at"] = datetime.now(timezone.utc)
        return True

    def get_user_id(self, sid_plain: str) -> Optional[str]:
        session = self._sessions.get(sid_plain)
        if not session:
            return None
        if session["revoked_at"] is not None:
            return None
        if session["expires_at"] <= datetime.now(timezone.utc):
            return None
        return session["user_id"]
