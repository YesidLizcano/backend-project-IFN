"""Dependency helpers to plug the auth microservice into FastAPI routes."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.Shared.Auth.Domain.auth_service_interface import (
    AuthServiceInterface,
    TokenPayload,
)
from src.Shared.Auth.External.auth_service_http import AuthServiceHttp

_http_bearer = HTTPBearer(auto_error=False)


def get_auth_service() -> AuthServiceInterface:
    """Provide a singleton-like AuthService instance for dependency injection."""

    return _get_cached_auth_service()


@lru_cache(maxsize=1)
def _get_cached_auth_service() -> AuthServiceInterface:
    """Instantiate the HTTP auth client once per process."""

    return AuthServiceHttp()


def get_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(_http_bearer),
    auth_service: AuthServiceInterface = Depends(get_auth_service),
) -> TokenPayload:
    """Validate the Authorization header and return the decoded token payload."""

    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token requerido")

    try:
        return auth_service.validate_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
