from datetime import date
from pydantic import BaseModel

from src.Modules.Conglomerados.Domain.subparcela import SubparcelaSalida


# --- 1. MODELO BASE (Componentes Comunes) ---
class MaterialEquipoBase(BaseModel):
    """Contiene los campos comunes que el usuario provee."""
    nombre: str
    cantidad: int

# --- 2. DTO de CREACIÓN (Entrada de la API) ---
class MaterialEquipoCrear(MaterialEquipoBase):
    """
    Hereda los campos base. Se usa para el cuerpo del POST.
    NO lleva municipio_id ni id.
    """
    pass

# --- 3. ENTIDAD DE DOMINIO ---
class MaterialEquipo(MaterialEquipoBase):
    """
    Hereda los campos base y añade los campos CLAVE para la lógica
    que son obligatorios en el Dominio.
    """
    departamento_id: int 

# --- 4. DTO de SALIDA (Respuesta de la API) ---
class MaterialEquipoSalida(MaterialEquipo):
    """
    Hereda la entidad de Dominio y añade los campos generados por la BD.
    """
    id: int

    class Config:
        from_attributes = True
