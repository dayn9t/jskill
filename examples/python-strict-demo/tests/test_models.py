"""Tests for domain models."""

import pytest
from pydantic import ValidationError

from demo.models import CreateUserRequest, User


class TestUser:
    """Test suite for User model."""

    def test_valid_user(self) -> None:
        """Should create user with valid data."""
        user = User(
            id="123",
            name="Alice",
            email="alice@example.com",
            status="active",
        )

        assert user.id == "123"
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.status == "active"

    def test_strict_mode_rejects_type_coercion(self) -> None:
        """Should reject type coercion in strict mode."""
        with pytest.raises(ValidationError):
            User(
                id=123,  # type: ignore[arg-type]  # int instead of str
                name="Alice",
                email="alice@example.com",
            )

    def test_extra_forbid_rejects_unknown_fields(self) -> None:
        """Should reject unknown fields."""
        with pytest.raises(ValidationError):
            User(
                id="123",
                name="Alice",
                email="alice@example.com",
                unknown_field="value",  # type: ignore[call-arg]
            )

    def test_frozen_prevents_mutation(self) -> None:
        """Should prevent mutation of frozen model."""
        user = User(id="123", name="Alice", email="alice@example.com")

        with pytest.raises(ValidationError):
            user.name = "Bob"  # type: ignore[misc]

    def test_invalid_email_rejected(self) -> None:
        """Should reject invalid email format."""
        with pytest.raises(ValidationError):
            User(id="123", name="Alice", email="invalid-email")

    def test_empty_name_rejected(self) -> None:
        """Should reject empty name."""
        with pytest.raises(ValidationError):
            User(id="123", name="", email="alice@example.com")

    def test_invalid_status_rejected(self) -> None:
        """Should reject invalid status literal."""
        with pytest.raises(ValidationError):
            User(
                id="123",
                name="Alice",
                email="alice@example.com",
                status="unknown",  # type: ignore[arg-type]
            )


class TestCreateUserRequest:
    """Test suite for CreateUserRequest model."""

    def test_valid_request(self) -> None:
        """Should create request with valid data."""
        request = CreateUserRequest(name="Alice", email="alice@example.com")

        assert request.name == "Alice"
        assert request.email == "alice@example.com"

    def test_strict_mode_rejects_type_coercion(self) -> None:
        """Should reject type coercion."""
        with pytest.raises(ValidationError):
            CreateUserRequest(
                name=123,  # type: ignore[arg-type]
                email="alice@example.com",
            )
