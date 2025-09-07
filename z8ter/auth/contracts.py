from __future__ import annotations
from typing import Protocol, Optional
from datetime import datetime


class SessionRepo(Protocol):
    def insert(
        self, *,
        sid_plain: str,
        user_id: str,
        expires_at: datetime,
        remember: bool,
        ip: Optional[str],
        user_agent: Optional[str],
        rotated_from_sid: Optional[str] = None,
    ) -> None: ...
    def revoke(self, *, sid_plain: str) -> bool: ...
    def get_user_id(self, sid_plain: str) -> Optional[str]: ...


class UserRepo(Protocol):
    def get_user_by_id(self, user_id: str) -> Optional[dict]: ...
