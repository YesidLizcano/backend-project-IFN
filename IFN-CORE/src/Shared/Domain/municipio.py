from pydantic import BaseModel


# --- 1. MODELO BASE (Componentes Comunes) ---
class MunicipioBase(BaseModel):
    """Contiene los campos comunes que el usuario provee."""
    nombre: str


# --- 2. DTO de CREACIÓN (Entrada de la API) ---
class MunicipioCrear(MunicipioBase):
    """
    Hereda los campos base. Se usa para el cuerpo del POST.
    NO lleva departamento_id ni id.
    """
    pass


# --- 3. ENTIDAD DE DOMINIO ---
class Municipio(MunicipioBase):
    """
    Hereda los campos base y añade los campos CLAVE para la lógica
    que son obligatorios en el Dominio.
    """
    departamento_id: int


# --- 4. DTO de SALIDA (Respuesta de la API) ---
class MunicipioSalida(Municipio):
    """
    Hereda la entidad de Dominio y añade los campos generados por la BD.
    """
    id: int

    class Config:
        from_attributes = True
