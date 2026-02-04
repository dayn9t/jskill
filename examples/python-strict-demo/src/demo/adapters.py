"""In-memory implementations for testing and development."""

from typing import TYPE_CHECKING

from demo.models import User

if TYPE_CHECKING:
    from demo.ports import Cache, UserRepository


class InMemoryUserRepository:
    """In-memory user repository implementation."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def get(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def save(self, user: User) -> str:
        self._users[user.id] = user
        return user.id

    def delete(self, user_id: str) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False


class InMemoryCache:
    """In-memory cache implementation."""

    def __init__(self) -> None:
        self._data: dict[str, object] = {}

    def get(self, key: str) -> object | None:
        return self._data.get(key)

    def set(self, key: str, value: object, ttl: int = 300) -> None:
        _ = ttl  # TTL ignored in memory implementation
        self._data[key] = value

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False


# Type check: verify implementations satisfy protocols
def _type_check() -> None:
    repo: UserRepository = InMemoryUserRepository()
    cache: Cache = InMemoryCache()
    _ = repo, cache
