import hmac
import hashlib
from datetime import datetime, timezone
from typing import Optional
from z8ter.db import get_conn


def _utcnow(): return datetime.now(timezone.utc)
def _iso(dt): return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class SidHasher:
    def __init__(self, key: bytes, k_id: str = "k1"):
        self.key, self.k_id = key, k_id

    def hash(self, sid_plain: str) -> str:
        return hmac.new(
            self.key, sid_plain.encode(), hashlib.sha256
        ).hexdigest()


class SessionRepo:
    def __init__(self, hasher: SidHasher):
        self.hasher = hasher

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
        sid_hash = self.hasher.hash(sid_plain)
        rotated_from_hash = (
            self.hasher.hash(rotated_from_sid) if rotated_from_sid else None
        )

        with get_conn() as c:
            c.execute(
                """
                INSERT INTO sessions (
                    sid_hash,
                    user_id,
                    created_at,
                    expires_at,
                    remember,
                    ip,
                    user_agent,
                    rotated_from_sid_hash,
                    revoked_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL)
                """,
                (
                    sid_hash,
                    user_id,
                    _iso(_utcnow()),
                    _iso(expires_at),
                    int(remember),
                    ip,
                    user_agent,
                    rotated_from_hash,
                ),
            )

    def revoke(self, *, sid_plain: str) -> bool:
        sid_hash = self.hasher.hash(sid_plain)
        with get_conn() as c:
            cur = c.execute(
                "UPDATE sessions SET revoked_at=? WHERE sid_hash=? AND "
                "revoked_at IS NULL",
                (_iso(_utcnow()), sid_hash),
            )
            return cur.rowcount > 0

    def get_user_id(self, sid) -> str:
        with get_conn() as c:
            c.execute(
                "UPDATE sessions SET revoked_at=? WHERE sid_hash=? AND "
                "revoked_at IS NULL",
                (_iso(_utcnow()), sid),
            )
            return "user_id"
