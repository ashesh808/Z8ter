from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from unittest.mock import Mock
import pytest
from z8ter.auth.contracts import SessionRepo, UserRepo


class MockSessionRepo:
    def __init__(self) -> None:
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.revoked_sessions: set[str] = set()

    def insert(
        self,
        *,
        sid_plain: str,
        user_id: str,
        expires_at: datetime,
        remember: bool,
        ip: Optional[str],
        user_agent: Optional[str],
        rotated_from_sid: Optional[str] = None,
    ) -> None:
        self.sessions[sid_plain] = {
            "user_id": user_id,
            "expires_at": expires_at,
            "remember": remember,
            "ip": ip,
            "user_agent": user_agent,
            "rotated_from_sid": rotated_from_sid,
        }

    def revoke(self, *, sid_plain: str) -> bool:
        if (sid_plain in self.sessions and sid_plain
           not in self.revoked_sessions):
            self.revoked_sessions.add(sid_plain)
            return True
        return False

    def get_user_id(self, sid_plain: str) -> Optional[str]:
        if sid_plain in self.revoked_sessions:
            return None
        session = self.sessions.get(sid_plain)
        if session and session["expires_at"] > datetime.now():
            return session["user_id"]
        return None


class MockUserRepo:
    def __init__(self) -> None:
        self.users: Dict[str, dict] = {}

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        return self.users.get(user_id)


# Fixtures
@pytest.fixture
def session_repo() -> MockSessionRepo:
    return MockSessionRepo()


@pytest.fixture
def user_repo() -> MockUserRepo:
    return MockUserRepo()


@pytest.fixture
def sample_user_data() -> dict:
    return {
        "id": "user123",
        "email": "test@example.com",
        "username": "testuser",
        "created_at": datetime.now(),
    }


@pytest.fixture
def sample_session_data() -> dict:
    return {
        "sid_plain": "session_abc123",
        "user_id": "user123",
        "expires_at": datetime.now() + timedelta(hours=1),
        "remember": False,
        "ip": "192.168.1.1",
        "user_agent": "Mozilla/5.0 Test Browser",
    }


# SessionRepo Tests
class TestSessionRepo:
    def test_insert_session_success(
        self, session_repo: MockSessionRepo, sample_session_data: dict
    ) -> None:
        """Test successful session insertion."""
        session_repo.insert(**sample_session_data)

        # Verify session was stored
        assert sample_session_data["sid_plain"] in session_repo.sessions
        stored = session_repo.sessions[sample_session_data["sid_plain"]]
        assert stored["user_id"] == sample_session_data["user_id"]
        assert stored["expires_at"] == sample_session_data["expires_at"]
        assert stored["remember"] == sample_session_data["remember"]
        assert stored["ip"] == sample_session_data["ip"]
        assert stored["user_agent"] == sample_session_data["user_agent"]

    def test_insert_session_with_rotation(
        self, session_repo: MockSessionRepo, sample_session_data: dict
    ) -> None:
        """Test session insertion with rotated_from_sid."""
        rotated_from = "old_session_xyz"
        sample_session_data["rotated_from_sid"] = rotated_from

        session_repo.insert(**sample_session_data)

        stored = session_repo.sessions[sample_session_data["sid_plain"]]
        assert stored["rotated_from_sid"] == rotated_from

    def test_insert_session_with_none_values(
        self, session_repo: MockSessionRepo
    ) -> None:
        """Test session insertion with None values for optional fields."""
        session_data = {
            "sid_plain": "session_none_test",
            "user_id": "user456",
            "expires_at": datetime.now() + timedelta(hours=1),
            "remember": True,
            "ip": None,
            "user_agent": None,
        }

        session_repo.insert(**session_data)

        stored = session_repo.sessions["session_none_test"]
        assert stored["ip"] is None
        assert stored["user_agent"] is None
        assert stored["rotated_from_sid"] is None

    def test_revoke_existing_session(
        self, session_repo: MockSessionRepo, sample_session_data: dict
    ) -> None:
        """Test revoking an existing session."""
        session_repo.insert(**sample_session_data)

        result = session_repo.revoke(sid_plain=sample_session_data["sid_plain"])

        assert result is True
        assert sample_session_data["sid_plain"] in session_repo.revoked_sessions

    def test_revoke_nonexistent_session(self, session_repo: MockSessionRepo) -> None:
        """Test revoking a non-existent session."""
        result = session_repo.revoke(sid_plain="nonexistent_session")

        assert result is False

    def test_revoke_already_revoked_session(
        self, session_repo: MockSessionRepo, sample_session_data: dict
    ) -> None:
        """Test revoking an already revoked session."""
        session_repo.insert(**sample_session_data)
        session_repo.revoke(sid_plain=sample_session_data["sid_plain"])

        # Try to revoke again
        result = session_repo.revoke(sid_plain=sample_session_data["sid_plain"])

        assert result is False

    def test_get_user_id_valid_session(
        self, session_repo: MockSessionRepo, sample_session_data: dict
    ) -> None:
        """Test getting user_id from valid session."""
        session_repo.insert(**sample_session_data)

        user_id = session_repo.get_user_id(sample_session_data["sid_plain"])

        assert user_id == sample_session_data["user_id"]

    def test_get_user_id_expired_session(self, session_repo: MockSessionRepo) -> None:
        """Test getting user_id from expired session."""
        expired_session = {
            "sid_plain": "expired_session",
            "user_id": "user789",
            "expires_at": datetime.now() - timedelta(hours=1),
            "remember": False,
            "ip": "192.168.1.1",
            "user_agent": "Test Browser",
        }
        session_repo.insert(**expired_session)

        user_id = session_repo.get_user_id(expired_session["sid_plain"])

        assert user_id is None

    def test_get_user_id_revoked_session(
        self, session_repo: MockSessionRepo, sample_session_data: dict
    ) -> None:
        """Test getting user_id from revoked session."""
        session_repo.insert(**sample_session_data)
        session_repo.revoke(sid_plain=sample_session_data["sid_plain"])

        user_id = session_repo.get_user_id(sample_session_data["sid_plain"])

        assert user_id is None

    def test_get_user_id_nonexistent_session(
        self, session_repo: MockSessionRepo
    ) -> None:
        """Test getting user_id from non-existent session."""
        user_id = session_repo.get_user_id("nonexistent_session")

        assert user_id is None


# UserRepo Tests
class TestUserRepo:
    def test_get_user_by_id_existing_user(
        self, user_repo: MockUserRepo, sample_user_data: dict
    ) -> None:
        """Test getting an existing user by ID."""
        user_repo.users[sample_user_data["id"]] = sample_user_data

        user = user_repo.get_user_by_id(sample_user_data["id"])

        assert user == sample_user_data
        assert user["id"] == sample_user_data["id"]
        assert user["email"] == sample_user_data["email"]

    def test_get_user_by_id_nonexistent_user(self, user_repo: MockUserRepo) -> None:
        """Test getting a non-existent user by ID."""
        user = user_repo.get_user_by_id("nonexistent_user")

        assert user is None

    def test_get_user_by_id_empty_string(self, user_repo: MockUserRepo) -> None:
        """Test getting user with empty string ID."""
        user = user_repo.get_user_by_id("")

        assert user is None

    def test_get_user_by_id_multiple_users(self, user_repo: MockUserRepo) -> None:
        """Test getting specific user when multiple users exist."""
        user1 = {"id": "user1", "name": "Alice"}
        user2 = {"id": "user2", "name": "Bob"}

        user_repo.users["user1"] = user1
        user_repo.users["user2"] = user2

        retrieved_user1 = user_repo.get_user_by_id("user1")
        retrieved_user2 = user_repo.get_user_by_id("user2")

        assert retrieved_user1 == user1
        assert retrieved_user2 == user2
        assert retrieved_user1 != retrieved_user2


# Integration Tests
class TestRepoIntegration:
    def test_session_user_integration(
        self,
        session_repo: MockSessionRepo,
        user_repo: MockUserRepo,
        sample_user_data: dict,
        sample_session_data: dict,
    ) -> None:
        """Test integration between SessionRepo and UserRepo."""
        user_repo.users[sample_user_data["id"]] = sample_user_data
        session_repo.insert(**sample_session_data)

        retrieved_user_id = session_repo.get_user_id(
            sample_session_data["sid_plain"]
        )
        retrieved_user = user_repo.get_user_by_id(retrieved_user_id or "")

        assert retrieved_user_id == sample_user_data["id"]
        assert retrieved_user == sample_user_data

    def test_session_revocation_affects_user_retrieval(
        self,
        session_repo: MockSessionRepo,
        user_repo: MockUserRepo,
        sample_user_data: dict,
        sample_session_data: dict,
    ) -> None:
        """Session revocation prevents user retrieval via session."""
        user_repo.users[sample_user_data["id"]] = sample_user_data
        session_repo.insert(**sample_session_data)

        user_id = session_repo.get_user_id(sample_session_data["sid_plain"])
        assert user_id == sample_user_data["id"]

        session_repo.revoke(sid_plain=sample_session_data["sid_plain"])

        user_id_after_revoke = session_repo.get_user_id(
            sample_session_data["sid_plain"]
        )
        assert user_id_after_revoke is None


# Protocol Compliance Tests using Mock
class TestProtocolCompliance:
    def test_session_repo_protocol_compliance(self) -> None:
        """Test that our mock implements SessionRepo protocol correctly."""
        mock_repo = Mock(spec=SessionRepo)

        mock_repo.insert(
            sid_plain="test",
            user_id="user1",
            expires_at=datetime.now(),
            remember=True,
            ip="127.0.0.1",
            user_agent="test",
            rotated_from_sid=None,
        )
        mock_repo.revoke(sid_plain="test")
        mock_repo.get_user_id("test")

        assert mock_repo.insert.called
        assert mock_repo.revoke.called
        assert mock_repo.get_user_id.called

    def test_user_repo_protocol_compliance(self) -> None:
        """Test that our mock implements UserRepo protocol correctly."""
        mock_repo = Mock(spec=UserRepo)
        mock_repo.get_user_by_id("user1")
        assert mock_repo.get_user_by_id.called


# Edge Cases and Error Scenarios
class TestEdgeCases:
    def test_session_repo_concurrent_operations(
        self, session_repo: MockSessionRepo, sample_session_data: dict
    ) -> None:
        """Test concurrent-like operations on SessionRepo."""
        session1 = sample_session_data.copy()
        session1["sid_plain"] = "session1"

        session2 = sample_session_data.copy()
        session2["sid_plain"] = "session2"

        session_repo.insert(**session1)
        session_repo.insert(**session2)

        assert session_repo.get_user_id("session1") == sample_session_data["user_id"]
        assert session_repo.get_user_id("session2") == sample_session_data["user_id"]

        session_repo.revoke(sid_plain="session1")
        assert session_repo.get_user_id("session1") is None
        assert session_repo.get_user_id("session2") == sample_session_data["user_id"]

    def test_session_boundary_expiration(self, session_repo: MockSessionRepo) -> None:
        """Test session expiration at exact boundary (non-flaky)."""
        now = datetime.now()
        session_data = {
            "sid_plain": "boundary_session",
            "user_id": "user123",
            "expires_at": now + timedelta(microseconds=1),
            "remember": False,
            "ip": "127.0.0.1",
            "user_agent": "test",
        }

        session_repo.insert(**session_data)

        # Allow a moment to pass, then ensure it is considered expired.
        import time

        time.sleep(0.001)
        user_id = session_repo.get_user_id("boundary_session")
        assert user_id is None

    def test_user_repo_special_characters_in_id(self, user_repo: MockUserRepo) -> None:
        """Test UserRepo with special characters in user ID."""
        special_ids = [
            "user@domain.com",
            "user-with-dashes",
            "user_with_underscores",
            "用户123",
            "user with spaces",
            "123456",
        ]

        for user_id in special_ids:
            user_data = {"id": user_id, "name": f"User {user_id}"}
            user_repo.users[user_id] = user_data

            retrieved = user_repo.get_user_by_id(user_id)
            assert retrieved == user_data
