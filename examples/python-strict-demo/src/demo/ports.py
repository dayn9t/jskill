"""Protocol definitions (ports) for dependency inversion."""

from typing import Protocol

from demo.models import User


class UserRepository(Protocol):
    """Abstract repository for user persistence."""

    def get(self, user_id: str) -> User | None: ...

    def save(self, user: User) -> str: ...

    def delete(self, user_id: str) -> bool: ...


class Cache(Protocol):
    """Abstract cache interface."""

    def get(self, key: str) -> object | None: ...

    def set(self, key: str, value: object, ttl: int = 300) -> None: ...

    def delete(self, key: str) -> bool: ...
