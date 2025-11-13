from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.Modules.Brigadas.Infrastructure.Persistence.integranteBrigada_db import IntegranteBrigadaDB
    from src.Modules.Conglomerados.Infrastructure.Persistence.conglomerado_db import ConglomeradoDB
    from src.Modules.MaterialEquipo.Infrastructure.Persistence.controlEquipo_db import ControlEquipoDB


class BrigadaDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conglomerado_id: int = Field(foreign_key="conglomeradodb.id", unique=True)
    fechaCreacion: date = Field(default=None)
    estado: str = Field(default=None)
    conglomerado: "ConglomeradoDB" = Relationship(back_populates="brigada")
    integrantes_brigada: list["IntegranteBrigadaDB"] = Relationship(back_populates="brigada")
    control_equipo: list["ControlEquipoDB"] = Relationship(back_populates="brigada")

from src.Modules.Brigadas.Infrastructure.Persistence import integranteBrigada_db
