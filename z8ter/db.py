import os
import sqlite3
from pathlib import Path

_DB_PATH = Path(os.getenv("Z8_DB_PATH", "./var/z8ter.sqlite3"))
_DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_conn() -> sqlite3.Connection:
    """
    Open a new SQLite connection with sane defaults.
    Call conn.close() when done (or use 'with get_conn() as conn:').
    """
    conn = sqlite3.connect(
        _DB_PATH,
        detect_types=sqlite3.PARSE_DECLTYPES,
        isolation_level=None,
        check_same_thread=False,
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn


def init_db():
    """Create tables if they don't exist (idempotent)."""
    ddl = """
    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY,
      email TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      email_verified_at TIMESTAMP NULL,
      deactivated_at TIMESTAMP NULL,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_conn() as conn:
        conn.executescript(ddl)
