from pydantic import BaseModel
from datetime import date
from typing import Optional


# --- 1. MODELO BASE (Componentes Comunes) ---
class ControlEquipoBase(BaseModel):
    """Contiene los campos comunes que el usuario provee."""
    cantidad_asignada: int
    fecha_Inicio_Asignacion: date
    fecha_Fin_Asignacion: Optional[date] = None
    

# --- 2. DTO de CREACIÓN (Entrada de la API) ---
class ControlEquipoCrear(ControlEquipoBase):
    """
    Hereda los campos base. Se usa para el cuerpo del POST.
    NO lleva id, id_material_equipo ni id_brigada (vienen del path).
    """
    pass


# --- 2b. DTO INTERNO con IDs para persistencia ---
class ControlEquipoGuardar(ControlEquipoBase):
    """
    Incluye los IDs necesarios para guardar en BD.
    Usado internamente en el caso de uso.
    """
    id_brigada: int
    id_material_equipo: int


# --- 3. ENTIDAD DE DOMINIO / DTO de SALIDA ---
class ControlEquipo(ControlEquipoBase):
    """
    Hereda los campos base y añade los campos CLAVE para la lógica
    que son obligatorios en el Dominio.
    """
    id: int
    id_material_equipo: int
    id_brigada: int
    

    class Config:
        from_attributes = True
