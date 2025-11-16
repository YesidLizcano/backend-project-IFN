from fastapi import HTTPException, status
from jose import JWTError
from src.Domain.autenticacion_repository import AutenticacionRepository
from src.Infrastructure.Core.seguridad import verificacion_password, crear_token_acceso, decodificar_token_acceso

class Autenticacion:
    def __init__(self, repository: AutenticacionRepository):
        self.repo = repository

    def login(self, email: str, password: str) -> dict:
        """Caso de uso: Autenticar y generar JWT y datos mínimos del usuario."""
        
        # 1. Obtener datos y hash del repositorio
        try:
            user_data = self.repo.obtener_datos_usuario(email)
        except Exception:
            # Error de DB o usuario no encontrado
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )

        # 2. Verificar la contraseña usando la utilidad de seguridad (bcrypt)
        if not verificacion_password(password, user_data['password_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )

        # 3. Generar nuestro token interno si es exitoso
        token_payload = {"sub": user_data['email'], "uid": user_data['uid']}
        token = crear_token_acceso(token_payload)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "name": user_data['name'],
                "email": user_data['email'],
            },
        }

    def validar_token(self, token: str) -> dict:
        """Caso de uso: Validar el token y obtener datos de usuario."""
        try:
            payload = decodificar_token_acceso(token)
            if payload.get("sub") is None or payload.get("uid") is None:
                 raise JWTError()
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado"
            )