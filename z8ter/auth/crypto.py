from argon2 import PasswordHasher
from argon2.low_level import Type

_PH = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16,
    type=Type.ID
)


def hash_password(plain: str) -> str:
    return _PH.hash(plain)


def verify_password(hash_: str, plain: str) -> bool:
    try:
        _PH.verify(hash_, plain)
        return True
    except Exception:
        return False


def needs_rehash(hash_: str) -> bool:
    return _PH.check_needs_rehash(hash_)
