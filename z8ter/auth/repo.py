import sqlite3
import uuid
from typing import Optional, TypedDict
from .crypto import hash_password


class User(TypedDict):
    id: str
    email: str
    password_hash: str
    email_verified_at: Optional[str]
    deactivated_at: Optional[str]
    created_at: str


def _row_to_user(row) -> User:
    return {
        "id": row[0],
        "email": row[1],
        "password_hash": row[2],
        "email_verified_at": row[3],
        "deactivated_at": row[4],
        "created_at": row[5]
    }


def get_user_email(conn: sqlite3.Connection, email: str) -> Optional[User]:
    cur = conn.execute(
        "SELECT "
        "id,email,password_hash,email_verified_at,deactivated_at,created_at "
        "FROM users WHERE email = ?",
        (email.lower(),)
        )
    row = cur.fetchone()
    return _row_to_user(row) if row else None


def create_user(
        conn: sqlite3.Connection,
        email: str,
        password: str
) -> User | None:
    user_id = str(uuid.uuid4())
    phash = hash_password(password)
    conn.execute(
        "INSERT INTO users (id,email,password_hash) VALUES (?,?,?)",
        (user_id, email.lower(), phash)
    )
    conn.commit()
    return get_user_email(conn, email)
