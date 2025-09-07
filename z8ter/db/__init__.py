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
