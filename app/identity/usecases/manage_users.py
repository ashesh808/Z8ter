from typing import Optional

from z8ter.auth.crypto import hash_password


class ManageUsers:
    def __init__(self, user_repo) -> None:
        self.user_repo = user_repo

    async def create_user(self, email: str, pwd: str) -> str:
        """Create a user and return its user_id."""
        user_id = email
        self.user_repo.add_user(
            user_id,
            {
                "id": user_id,
                "email": email,
                "pwd_hash": hash_password(pwd),
            },
        )
        return user_id

    async def get_user_email(self, email: str) -> Optional[dict]:
        """Fetch user record by email."""
        return self.user_repo.get_user_by_id(email)
