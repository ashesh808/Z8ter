from __future__ import annotations

from z8ter.auth.crypto import hash_password, needs_rehash, verify_password


def test_hash_and_verify_password_roundtrip() -> None:
    raw = "sup3r-secret!"
    hashed = hash_password(raw)

    assert hashed.startswith("$argon2id$")
    assert hashed != raw
    assert verify_password(hashed, raw)
    assert not verify_password(hashed, "not-the-right-password")


def test_needs_rehash_is_false_for_fresh_hash() -> None:
    hashed = hash_password("another-secret")
    # A freshly generated hash should already match the current parameters.
    assert not needs_rehash(hashed)
