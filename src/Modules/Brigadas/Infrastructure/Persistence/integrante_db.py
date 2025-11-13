from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from src.Shared.Infrastructure.Persistence.municipio_db import MunicipioDB
    from src.Modules.Brigadas.Infrastructure.Persistence.integranteBrigada_db import IntegranteBrigadaDB

class IntegranteDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estado: str = Field(default=None)
    nombreCompleto: str = Field(default=None)
    jefeBrigada: bool = Field(default=False)
    botanico: bool = Field(default=False)
    auxiliar: bool = Field(default=False)
    coinvestigador: bool = Field(default=False)
    telefono: str = Field(default=None)
    email: str = Field(default=None)
    municipio_id: int = Field(foreign_key="municipiodb.id")
    municipio: "MunicipioDB" = Relationship(back_populates="integrantes")
    brigadas_integrante: list["IntegranteBrigadaDB"] = Relationship(back_populates="integrante")

from src.Modules.Brigadas.Infrastructure.Persistence import integranteBrigada_db