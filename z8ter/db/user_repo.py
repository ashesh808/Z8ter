import uuid
from typing import Optional, TypedDict
from z8ter.auth.crypto import hash_password
from z8ter.db import get_conn


class User(TypedDict):
    id: str
    email: str
    password_hash: str
    email_verified_at: Optional[str]
    deactivated_at: Optional[str]
    created_at: str


class UserRepo:
    def __init__(self) -> None:
        self.conn = get_conn()

    def _row_to_user(self, row) -> User:
        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "email_verified_at": row[3],
            "deactivated_at": row[4],
            "created_at": row[5]
        }

    def get_user_email(
            self,
            email: str
    ) -> Optional[User]:
        cur = self.conn.execute(
            "SELECT "
            "id,"
            "email,"
            "password_hash,email_verified_at,deactivated_at,created_at "
            "FROM users WHERE email = ?",
            (email.lower(),)
            )
        row = cur.fetchone()
        return self._row_to_user(row) if row else None

    def create_user(
            self,
            email: str,
            password: str
    ) -> User | None:
        user_id = str(uuid.uuid4())
        phash = hash_password(password)
        self.conn.execute(
            "INSERT INTO users (id,email,password_hash) VALUES (?,?,?)",
            (user_id, email.lower(), phash)
        )
        self.conn.commit()
        return self.get_user_email(email)

    def get_user_by_id(self, user_id: str):
        cur = self.conn.execute(
            "SELECT "
            "id,"
            "email,"
            "password_hash,"
            "email_verified_at,deactivated_at,created_at "
            "FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "email_verified_at": row[3],
            "deactivated_at": row[4],
            "created_at": row[5]
        }
