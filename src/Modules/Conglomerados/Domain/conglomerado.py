# from typing import TYPE_CHECKING
# from geoalchemy2 import Geography
from datetime import date
# from sqlmodel import Column, Field, Relationship,  SQLModel, Field


from pydantic import BaseModel

from src.Modules.Conglomerados.Domain.subparcela import SubparcelaSalida


# --- 1. MODELO BASE (Componentes Comunes) ---
class ConglomeradoBase(BaseModel):
    """Contiene los campos comunes que el usuario provee."""
    fechaInicio: date
    fechaFinAprox: date | None
    fechaFin: date 
    latitud: float
    longitud: float

# --- 2. DTO de CREACIÓN (Entrada de la API) ---
class ConglomeradoCrear(ConglomeradoBase):
    """
    Hereda los campos base. Se usa para el cuerpo del POST.
    NO lleva municipio_id ni id.
    """
    pass

# --- 3. ENTIDAD DE DOMINIO ---
class Conglomerado(ConglomeradoBase):
    """
    Hereda los campos base y añade los campos CLAVE para la lógica
    que son obligatorios en el Dominio.
    """
    municipio_id: int 

# --- 4. DTO de SALIDA (Respuesta de la API) ---
class ConglomeradoSalida(Conglomerado):
    """
    Hereda la entidad de Dominio y añade los campos generados por la BD.
    """
    id: int
    subparcelas: list[SubparcelaSalida] = []

    class Config:
        from_attributes = True

# if TYPE_CHECKING:
#     from src.Shared.Domain.municipio import Municipio

# class ConglomeradoBase(SQLModel):
#     fechaInicio: date = Field(default=None)
#     fechaFinAprox: date | None = Field(default=None)
#     fechaFin: date = Field(default=None)

# class Conglomerado(ConglomeradoBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     municipio_id: int = Field(foreign_key="municipio.id")
#     municipio: "Municipio" = Relationship(back_populates="conglomerados")
#     # Campo PostGIS: GEOGRAPHY(Point, 4326)
#     ubicacion: str = Field(
#             sa_column=Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
#         )

# class CrearConglomerado(ConglomeradoBase):
#     latitud: float
#     longitud: float
#     pass

