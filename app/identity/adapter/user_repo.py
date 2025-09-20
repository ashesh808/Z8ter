from __future__ import annotations

from typing import Optional


class InMemoryUserRepo:
    def __init__(self) -> None:
        self._users: dict[str, dict] = {}

    def add_user(self, user_id: str, user: dict) -> None:
        """Convenience helper for tests/dev only."""
        self._users[user_id] = user

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        return self._users.get(user_id)
