"""Domain models with strict Pydantic validation."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    """User entity with strict validation."""

    model_config = ConfigDict(
        strict=True,
        extra="forbid",
        frozen=True,
    )

    id: str
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    status: Literal["active", "inactive"] = "active"


class CreateUserRequest(BaseModel):
    """Request model for creating a user."""

    model_config = ConfigDict(
        strict=True,
        extra="forbid",
    )

    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
