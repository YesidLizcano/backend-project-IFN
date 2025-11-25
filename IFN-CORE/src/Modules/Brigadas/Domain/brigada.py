from datetime import date
from pydantic import BaseModel, Field

from src.Modules.Brigadas.Domain.integrante import IntegranteSalida


class AsignacionIntegrante(BaseModel):
    """Representa la asignación de un integrante a una brigada."""
    integrante_id: int
    rol_asignado: str


# --- 1. MODELO BASE (Componentes Comunes) ---
class BrigadaBase(BaseModel):
    """Contiene los campos comunes que el usuario provee."""
    fechaCreacion: date
    estado: str


# --- 2. DTO de CREACIÓN (Entrada de la API) ---
class BrigadaCrear(BrigadaBase):
    """
    Hereda los campos base. Se usa para el cuerpo del POST.
    NO lleva municipio_id ni id.
    """
    fechaInicio: date
    fechaFinAprox: date
    integrantes_asignados: list[AsignacionIntegrante] = Field(default_factory=list)

# --- 3. ENTIDAD DE DOMINIO ---
class Brigada(BrigadaBase):
    """
    Hereda los campos base y añade los campos CLAVE para la lógica
    que son obligatorios en el Dominio.
    """
    conglomerado_id: int 

# --- 4. DTO de SALIDA (Respuesta de la API) ---
class BrigadaSalida(Brigada):
    """
    Hereda la entidad de Dominio y añade los campos generados por la BD.
    """
    id: int
    integrantes: str

    class Config:
        from_attributes = True