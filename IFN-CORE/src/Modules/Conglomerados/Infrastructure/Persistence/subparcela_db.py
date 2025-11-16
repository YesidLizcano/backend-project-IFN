from typing import TYPE_CHECKING
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship
from geoalchemy2 import Geography
from datetime import date

if TYPE_CHECKING:
    from src.Modules.Conglomerados.Infrastructure.Persistence.conglomerado_db import ConglomeradoDB

class SubparcelaDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conglomerado_id: int = Field(foreign_key="conglomeradodb.id")
    latitud: float = Field(default=None)
    longitud: float = Field(default=None)
    conglomerado: "ConglomeradoDB" = Relationship(back_populates="subparcelas")