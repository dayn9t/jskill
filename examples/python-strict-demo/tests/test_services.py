"""Tests for user service."""

from demo.adapters import InMemoryCache, InMemoryUserRepository
from demo.models import CreateUserRequest
from demo.result import Err, Ok
from demo.services import UserService


class TestUserService:
    """Test suite for UserService."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.repo = InMemoryUserRepository()
        self.cache = InMemoryCache()
        self.service = UserService(repo=self.repo, cache=self.cache)

    def test_create_user_success(self) -> None:
        """Should create a user successfully."""
        request = CreateUserRequest(name="Alice", email="alice@example.com")

        result = self.service.create_user(request)

        assert isinstance(result, Ok)
        assert result.value.name == "Alice"
        assert result.value.email == "alice@example.com"
        assert result.value.status == "active"

    def test_get_user_not_found(self) -> None:
        """Should return error when user not found."""
        result = self.service.get_user("nonexistent")

        assert isinstance(result, Err)
        assert "not found" in result.error

    def test_get_user_from_cache(self) -> None:
        """Should return user from cache on second call."""
        request = CreateUserRequest(name="Bob", email="bob@example.com")
        create_result = self.service.create_user(request)
        assert isinstance(create_result, Ok)
        user_id = create_result.value.id

        # First call - from repo
        result1 = self.service.get_user(user_id)
        assert isinstance(result1, Ok)

        # Second call - from cache
        result2 = self.service.get_user(user_id)
        assert isinstance(result2, Ok)
        assert result1.value == result2.value

    def test_delete_user_success(self) -> None:
        """Should delete user successfully."""
        request = CreateUserRequest(name="Charlie", email="charlie@example.com")
        create_result = self.service.create_user(request)
        assert isinstance(create_result, Ok)
        user_id = create_result.value.id

        result = self.service.delete_user(user_id)

        assert isinstance(result, Ok)
        assert result.value is True

    def test_delete_user_not_found(self) -> None:
        """Should return error when deleting nonexistent user."""
        result = self.service.delete_user("nonexistent")

        assert isinstance(result, Err)
        assert "not found" in result.error
