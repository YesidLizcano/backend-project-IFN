from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

from src.Modules.Brigadas.Infrastructure.Persistence.brigada_db import BrigadaDB

if TYPE_CHECKING:
    from src.Shared.Infrastructure.Persistence.municipio_db import MunicipioDB
    from src.Modules.Conglomerados.Infrastructure.Persistence.subparcela_db import SubparcelaDB

class ConglomeradoDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fechaInicio: date = Field(default=None)
    fechaFinAprox: date = Field(default=None)
    fechaFin: date | None = Field(default=None)
    municipio_id: int = Field(foreign_key="municipiodb.id")
    latitud: float = Field(default=None)
    longitud: float = Field(default=None)
    municipio: "MunicipioDB" = Relationship(back_populates="conglomerados")
    subparcelas: list["SubparcelaDB"] = Relationship(back_populates="conglomerado")
    brigada: "BrigadaDB" = Relationship(back_populates="conglomerado")