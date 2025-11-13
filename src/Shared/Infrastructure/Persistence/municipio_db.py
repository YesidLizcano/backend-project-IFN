from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from src.Modules.Brigadas.Infrastructure.Persistence.integrante_db import IntegranteDB

if TYPE_CHECKING:
    from src.Shared.Infrastructure.Persistence.departamento_db import DepartamentoDB
    from src.Modules.Conglomerados.Infrastructure.Persistence.conglomerado_db import ConglomeradoDB

class MunicipioDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(default=None)
    departamento_id: int = Field(foreign_key="departamentodb.id")
    departamento: "DepartamentoDB" = Relationship(back_populates="municipios")
    conglomerados: list["ConglomeradoDB"] = Relationship(back_populates="municipio")
    integrantes: list["IntegranteDB"] = Relationship(back_populates="municipio")
