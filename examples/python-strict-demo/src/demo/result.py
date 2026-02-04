"""Result type for explicit error handling."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Ok[T]:
    """Success result containing a value."""

    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class Err[E]:
    """Error result containing an error."""

    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True


type Result[T, E] = Ok[T] | Err[E]
