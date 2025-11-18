"""Domain contract for Auth services used across the project."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, TypedDict


class TokenPayload(TypedDict):
    """Shape of the payload returned by the auth microservice."""

    sub: str
    uid: str


class AuthServiceInterface(Protocol):
    """ProtocolAthat describes the behaviour expected from any auth service."""

    def validate_token(self, token: str) -> TokenPayload:
        """Validate a bearer token and return the decoded payload."""


class AbstractAuthService(ABC):
    """Abstract base class for services that talk to the auth microservice."""

    @abstractmethod
    def validate_token(self, token: str) -> TokenPayload:
        """Validate a bearer token and return the decoded payload."""
        raise NotImplementedError
