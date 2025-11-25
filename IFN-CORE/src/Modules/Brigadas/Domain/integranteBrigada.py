from pydantic import BaseModel

from src.Modules.Brigadas.Domain.integrante import StatusEnum
from src.Modules.Conglomerados.Domain.subparcela import SubparcelaSalida


# --- 1. MODELO BASE (Componentes Comunes) ---
class IntegranteBrigadaBase(BaseModel):
    """Contiene los campos comunes que el usuario provee."""
    rol: str
    

# --- 2. DTO de CREACIÓN (Entrada de la API) ---
class IntegranteBrigadaCrear(IntegranteBrigadaBase):
    """
    Hereda los campos base. Se usa para el cuerpo del POST.
    NO lleva municipio_id ni id.
    """
    pass

# --- 3. ENTIDAD DE DOMINIO / DTO de SALIDA ---
class IntegranteBrigada(IntegranteBrigadaBase):
    """
    Hereda los campos base y añade los campos CLAVE para la lógica
    que son obligatorios en el Dominio.
    """
    id_brigada: int 
    id_integrante: int
    

    class Config:
        from_attributes = True


class IntegranteBrigadaRolSalida(BaseModel):
    """Representa el rol asignado y datos básicos del integrante dentro de una brigada."""
    id_brigada: int
    id_integrante: int
    rol: str | None = None
    nombreCompleto: str | None = None
    telefono: str | None = None
    email: str | None = None
    estado: StatusEnum | None = None