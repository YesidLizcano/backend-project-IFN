from fastapi import Depends
from sqlmodel import Session, select
from src.Shared.Domain.municipio import Municipio, MunicipioSalida
from src.Shared.Domain.municipio_repository import MunicipioRepository
from src.Shared.Infrastructure.Persistence.database import get_session
from src.Shared.Infrastructure.Persistence.municipio_db import MunicipioDB


class SQLAlchemyMunicipioRepository(MunicipioRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, municipio: Municipio) -> MunicipioSalida:
        db_municipio = MunicipioDB(**municipio.model_dump())
        self.db.add(db_municipio)
        self.db.commit()
        self.db.refresh(db_municipio)
        return MunicipioSalida.model_validate(db_municipio)

    def buscar_por_id(self, municipio_id: int) -> Municipio | None:
        db_municipio = self.db.get(MunicipioDB, municipio_id)
        return Municipio.model_validate(db_municipio) if db_municipio else None

    def listar_municipios(self) -> list[MunicipioSalida]:
        return self.db.exec(select(MunicipioDB)).all()

def get_municipio_repository(
    session: Session = Depends(get_session),
) -> MunicipioRepository:
    return SQLAlchemyMunicipioRepository(session)