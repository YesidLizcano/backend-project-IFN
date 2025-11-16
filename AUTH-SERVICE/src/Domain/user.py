from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Schema para la petición de login (JSON)."""
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    name: str
    email: EmailStr


class LoginResponse(BaseModel):
    """Respuesta de login: token + datos mínimos del usuario."""
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class TokenData(BaseModel):
    """Datos decodificados del token."""
    sub: str  # email
    uid: str


class Token(BaseModel):
    """Token simple de acceso para respuestas de login minimalistas."""
    access_token: str
    token_type: str = "bearer"
