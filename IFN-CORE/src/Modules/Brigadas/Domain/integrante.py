from datetime import date
from enum import Enum
from pydantic import BaseModel

from src.Modules.Conglomerados.Domain.subparcela import SubparcelaSalida


# --- 1. MODELO BASE (Componentes Comunes) ---
class IntegranteBase(BaseModel):
    """Contiene los campos comunes que el usuario provee."""
    estado: str
    nombreCompleto: str
    jefeBrigada: bool 
    botanico: bool
    auxiliar: bool
    coinvestigador: bool
    telefono: str
    email: str
    

class StatusEnum(str, Enum):
    """Enumeración de estados permitidos para un integrante."""
    ACTIVO_DISPONIBLE = "ACTIVO_DISPONIBLE"
    ACTIVO_VACACIONES = "ACTIVO_VACACIONES"
    ACTIVO_INCAPACITADO = "ACTIVO_INCAPACITADO"
    ACTIVO_NO_DISPONIBLE = "ACTIVO_NO_DISPONIBLE"
    BLOQUEADO = "BLOQUEADO"
    INACTIVO = "INACTIVO"

# --- 2. DTO de CREACIÓN (Entrada de la API) ---
class IntegranteCrear(IntegranteBase):
    """
    Hereda los campos base. Se usa para el cuerpo del POST.
    NO lleva municipio_id ni id.
    """
    pass

# --- 3. ENTIDAD DE DOMINIO ---
class Integrante(IntegranteBase):
    """
    Hereda los campos base y añade los campos CLAVE para la lógica
    que son obligatorios en el Dominio.
    """
    municipio_id: int 

# --- 4. DTO de SALIDA (Respuesta de la API) ---
class IntegranteSalida(Integrante):
    """
    Hereda la entidad de Dominio y añade los campos generados por la BD.
    """
    id: int

    class Config:
        from_attributes = True


class IntegranteActualizar(BaseModel):
    """Campos opcionales para actualización parcial de un integrante."""
    estado: str | None = None
    nombreCompleto: str | None = None
    jefeBrigada: bool | None = None
    botanico: bool | None = None
    auxiliar: bool | None = None
    coinvestigador: bool | None = None
    telefono: str | None = None
    email: str | None = None
    municipio_id: int | None = None