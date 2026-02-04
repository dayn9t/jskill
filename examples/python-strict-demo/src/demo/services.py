"""User service with dependency injection."""

import uuid
from dataclasses import dataclass

from demo.models import CreateUserRequest, User
from demo.ports import Cache, UserRepository
from demo.result import Err, Ok, Result


@dataclass
class UserService:
    """User business logic with injected dependencies."""

    repo: UserRepository
    cache: Cache

    def get_user(self, user_id: str) -> Result[User, str]:
        """Get user by ID, checking cache first."""
        # Check cache
        cached = self.cache.get(f"user:{user_id}")
        if cached is not None and isinstance(cached, User):
            return Ok(cached)

        # Query repository
        user = self.repo.get(user_id)
        if user is None:
            return Err(f"User not found: {user_id}")

        # Cache result
        self.cache.set(f"user:{user_id}", user)
        return Ok(user)

    def create_user(self, request: CreateUserRequest) -> Result[User, str]:
        """Create a new user."""
        user = User(
            id=str(uuid.uuid4()),
            name=request.name,
            email=request.email,
            status="active",
        )

        try:
            self.repo.save(user)
        except Exception as e:
            return Err(f"Failed to save user: {e}")

        return Ok(user)

    def delete_user(self, user_id: str) -> Result[bool, str]:
        """Delete a user by ID."""
        if not self.repo.delete(user_id):
            return Err(f"User not found: {user_id}")

        self.cache.delete(f"user:{user_id}")
        return Ok(True)
