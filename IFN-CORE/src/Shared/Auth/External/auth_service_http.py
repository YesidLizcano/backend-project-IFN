"""HTTP client that delegates token validation to the auth microservice."""

from __future__ import annotations

from typing import Final

import httpx
import os

from src.Shared.Auth.Domain.auth_service_interface import (
    AbstractAuthService,
    TokenPayload,
)


class AuthServiceHttp(AbstractAuthService):
    """Concrete Auth service that talks to the external auth API over HTTP."""

    def __init__(
        self,
        base_url: str = None,
        validate_token_path: str = "/auth/validar-token",
        timeout_seconds: float = 5.0,
    ) -> None:
        if base_url is None:
            base_url = os.environ.get("AUTH_SERVICE_URL")
        self._base_url: Final[str] = base_url.rstrip("/")
        self._validate_token_path: Final[str] = validate_token_path
        self._timeout_seconds: Final[float] = timeout_seconds

    def validate_token(self, token: str) -> TokenPayload:
        """Validate the provided token with the auth microservice."""

        if not token:
            raise ValueError("El token proporcionado está vacío")

        url = f"{self._base_url}{self._validate_token_path}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

        try:
            response = httpx.post(url, headers=headers, timeout=self._timeout_seconds)
        except httpx.HTTPError as exc:
            raise RuntimeError("No se pudo contactar al servicio de autenticación") from exc

        if response.status_code != httpx.codes.OK:
            raise ValueError(
                f"Token inválido o rechazado por el servicio de autenticación (status {response.status_code})"
            )

        data = response.json()
        return TokenPayload(sub=data["sub"], uid=data["uid"])
