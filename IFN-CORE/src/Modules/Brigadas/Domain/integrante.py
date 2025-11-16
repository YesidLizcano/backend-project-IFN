from datetime import date
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