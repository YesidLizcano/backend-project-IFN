import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv

# --- Configuración de Seguridad ---
# Cargar variables desde .env
load_dotenv()
# El bcrypt es necesario para verificar el hash de tu usuario de la base de datos.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT (desde .env con valores por defecto razonables)
LLAVE_SECRETA = os.getenv("LLAVE_SECRETA", "SECRET_KEY_DEL_AUTH_SERVICE_CAMBIAR_EN_PROD")
ALGORITMO = os.getenv("ALGORITMO", "HS256")
try:
    TOKEN_ACCESO_EXPIRA_MINUTOS = int(os.getenv("TOKEN_ACCESO_EXPIRA_MINUTOS", "60"))
except ValueError:
    TOKEN_ACCESO_EXPIRA_MINUTOS = 60

# --- Hashing ---
def verificacion_password(plain_password, hashed_password):
    """Verifica si la contraseña coincide con el hash evitando errores de backend."""
    try:
        pw_bytes = plain_password.encode("utf-8") if isinstance(plain_password, str) else plain_password
        if pw_bytes and len(pw_bytes) > 72:
            return False
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

# --- JWT ---
def crear_token_acceso(data: dict):
    """Crea un token de acceso JWT con tiempo de expiración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_ACCESO_EXPIRA_MINUTOS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, LLAVE_SECRETA, algorithm=ALGORITMO)
    return encoded_jwt

def decodificar_token_acceso(token: str):
    """Decodifica el token para obtener el payload. Lanza excepción si es inválido."""
    return jwt.decode(token, LLAVE_SECRETA, algorithms=[ALGORITMO])