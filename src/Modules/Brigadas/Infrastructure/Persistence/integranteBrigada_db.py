from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from src.Modules.Brigadas.Infrastructure.Persistence.brigada_db import BrigadaDB
    from src.Modules.Brigadas.Infrastructure.Persistence.integrante_db import IntegranteDB


class IntegranteBrigadaDB(SQLModel, table=True):
    id_brigada: int = Field(foreign_key="brigadadb.id", primary_key=True)
    id_integrante: int = Field(foreign_key="integrantedb.id", primary_key=True)
    rol: str = Field(default=None)
    brigada: "BrigadaDB" = Relationship(back_populates="integrantes_brigada")
    integrante: "IntegranteDB" = Relationship(back_populates="brigadas_integrante")
    