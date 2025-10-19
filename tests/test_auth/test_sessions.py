from __future__ import annotations

import asyncio
from http.cookies import SimpleCookie

from z8ter.auth.sessions import SessionManager
from z8ter.responses import Response


class _Repo:
    def __init__(self) -> None:
        self.insert_calls: list[dict] = []
        self.revoked: list[str] = []

    def insert(self, **kwargs) -> None:
        self.insert_calls.append(kwargs)

    def revoke(self, *, sid_plain: str) -> bool:
        self.revoked.append(sid_plain)
        return sid_plain == "known"

    def get_user_id(self, sid_plain: str) -> str | None:  # pragma: no cover
        return None


def test_start_session_persists_and_returns_sid() -> None:
    repo = _Repo()
    manager = SessionManager(session_repo=repo)

    sid = asyncio.run(
        manager.start_session(
            "user-1",
            remember=True,
            ip="1.1.1.1",
            user_agent="pytest",
            ttl=30,
        )
    )

    assert isinstance(sid, str) and sid
    assert len(repo.insert_calls) == 1
    call = repo.insert_calls[0]
    assert call["user_id"] == "user-1"
    assert call["remember"] is True
    assert call["ip"] == "1.1.1.1"
    assert call["user_agent"] == "pytest"
    assert call["expires_at"].tzinfo is not None


def test_revoke_session_delegates_to_repo() -> None:
    repo = _Repo()
    manager = SessionManager(session_repo=repo)

    assert asyncio.run(manager.revoke_session("known")) is True
    assert asyncio.run(manager.revoke_session("unknown")) is False
    assert repo.revoked == ["known", "unknown"]


def test_set_session_cookie_writes_expected_flags() -> None:
    repo = _Repo()
    manager = SessionManager(session_repo=repo)
    response = Response()

    asyncio.run(
        manager.set_session_cookie(
            response,
            sid="cookie-123",
            secure=False,
            remember=True,
            ttl=42,
        )
    )

    header = response.headers["set-cookie"]
    assert "HttpOnly" in header
    assert "Secure" not in header
    assert "Max-Age=42" in header

    cookie = SimpleCookie()
    cookie.load(header)
    assert cookie["z8_auth_sid"].value == "cookie-123"


def test_clear_session_cookie_marks_cookie_for_deletion() -> None:
    repo = _Repo()
    manager = SessionManager(session_repo=repo)
    response = Response()

    asyncio.run(manager.clear_session_cookie(response))
    header = response.headers["set-cookie"]
    assert "z8_auth_sid=" in header
    assert "Max-Age=0" in header or "expires=" in header.lower()
