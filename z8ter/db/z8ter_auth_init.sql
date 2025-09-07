CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  email_verified_at TIMESTAMP NULL,
  deactivated_at TIMESTAMP NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
  sid_hash        TEXT PRIMARY KEY,
  user_id         TEXT NOT NULL,
  created_at      TEXT NOT NULL,
  last_seen_at    TEXT,
  expires_at      TEXT NOT NULL,
  revoked_at      TEXT,
  remember        INTEGER NOT NULL DEFAULT 0,
  rotated_from    TEXT,
  ip              TEXT,
  user_agent      TEXT,
  k_id            TEXT DEFAULT 'k1',
  hash_alg        TEXT DEFAULT 'sha256',
  CONSTRAINT fk_sessions_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_sessions_sid_hash ON sessions(sid_hash);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_active ON sessions(revoked_at, expires_at);
CREATE INDEX IF NOT EXISTS idx_sessions_rotated_from ON sessions(rotated_from);