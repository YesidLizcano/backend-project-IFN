from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.Application.autenticacion import Autenticacion
from src.Domain.user import LoginRequest, TokenData, LoginResponse
from src.Infrastructure.Persistence.DBAutenticacionRepository import FirebaseAuthRepository

# --- Inyección de Dependencias ---
def get_autenticacion() -> Autenticacion:
    """Crea la dependencia de Autenticacion con el Repositorio concreto."""
    repository = FirebaseAuthRepository()
    return Autenticacion(repository)

# --- Rutas ---
# Seguridad: esquema HTTP Bearer para que el Authorize solo pida el token
security = HTTPBearer()
router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=LoginResponse)
async def login_for_access_token(
    request: LoginRequest, 
    service: Autenticacion = Depends(get_autenticacion)
):
    """Endpoint para autenticar al usuario y generar un token."""
    try:
        return service.login(request.email, request.password)
    except HTTPException as e:
        raise e # Re-lanza el 401 de la capa de Aplicación

@router.post("/validar-token", response_model=TokenData)
async def validar_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    autenticacion: Autenticacion = Depends(get_autenticacion)
):
    """Endpoint usado por IFN-CORE para validar que el token es legítimo y no ha expirado."""
    token = credentials.credentials
    payload = autenticacion.validar_token(token)
    
    # La respuesta usa el esquema TokenData que hereda de UserBase del Dominio
    return TokenData(**payload)