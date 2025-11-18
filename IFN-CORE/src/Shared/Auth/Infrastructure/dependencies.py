"""Dependency helpers to plug the auth microservice into FastAPI routes."""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.Shared.Auth.Domain.auth_service_interface import (
    AuthServiceInterface,
    TokenPayload,
)
from src.Shared.Auth.External.auth_service_http import AuthServiceHttp


class AuthDependencies:
    """Clase que encapsula las dependencias de autenticación."""
    
    _http_bearer = HTTPBearer(auto_error=False)
    _cached_service: AuthServiceInterface | None = None
    
    @classmethod
    def get_auth_service(cls) -> AuthServiceInterface:
        """Provide a singleton-like AuthService instance for dependency injection."""
        if cls._cached_service is None:
            cls._cached_service = AuthServiceHttp()
        return cls._cached_service
    
    @classmethod
    def get_token_payload(
        cls,
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


# Alias de las funciones de clase para usar directamente
get_auth_service = AuthDependencies.get_auth_service
get_token_payload = AuthDependencies.get_token_payload
