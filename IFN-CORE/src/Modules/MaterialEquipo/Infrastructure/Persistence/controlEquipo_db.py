from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.Modules.Brigadas.Infrastructure.Persistence.brigada_db import BrigadaDB
    from src.Modules.MaterialEquipo.Infrastructure.Persistence.materialEquipo_db import MaterialEquipoDB


class ControlEquipoDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_material_equipo: int = Field(foreign_key="materialequipodb.id")
    id_brigada: int = Field(foreign_key="brigadadb.id")
    cantidad_asignada: int = Field(default=None)
    fecha_Inicio_Asignacion: date = Field(default=None)
    fecha_Fin_Asignacion: date | None = Field(default=None)
    material_equipo: "MaterialEquipoDB" = Relationship(back_populates="control_equipo" )
    brigada: "BrigadaDB" = Relationship(back_populates="control_equipo")