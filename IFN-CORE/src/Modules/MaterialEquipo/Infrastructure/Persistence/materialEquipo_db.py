from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.Modules.MaterialEquipo.Infrastructure.Persistence.controlEquipo_db import ControlEquipoDB
    from src.Modules.Ubicacion.Infrastructure.Persistence.departamento_db import DepartamentoDB


class MaterialEquipoDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(default=None)
    cantidad: int = Field(default=None)
    departamento_id: int = Field(foreign_key="departamentodb.id")
    departamento: "DepartamentoDB" = Relationship(back_populates="material_equipo")
    control_equipo: list["ControlEquipoDB"] = Relationship(back_populates="material_equipo")