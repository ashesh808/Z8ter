from __future__ import annotations

from typing import Protocol

from z8ter.auth.contracts import SessionRepo, UserRepo


def test_auth_contracts_define_expected_methods() -> None:
    assert issubclass(SessionRepo, Protocol)
    assert {"insert", "revoke", "get_user_id"}.issubset(SessionRepo.__dict__)

    assert issubclass(UserRepo, Protocol)
    assert "get_user_by_id" in UserRepo.__dict__
