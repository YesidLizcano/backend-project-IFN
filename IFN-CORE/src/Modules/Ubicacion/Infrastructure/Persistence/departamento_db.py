from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.Modules.Ubicacion.Infrastructure.Persistence.municipio_db import MunicipioDB
    from src.Modules.MaterialEquipo.Infrastructure.Persistence.materialEquipo_db import MaterialEquipoDB

class DepartamentoDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(default=None)
    municipios: list["MunicipioDB"] = Relationship(back_populates="departamento")
    material_equipo: list["MaterialEquipoDB"] = Relationship(back_populates="departamento")