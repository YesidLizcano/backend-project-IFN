from fastapi import Depends
from sqlmodel import Session, select
from src.Modules.Ubicacion.Domain.municipio import Municipio, MunicipioSalida
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository
from src.Shared.database import get_session
from src.Modules.Ubicacion.Infrastructure.Persistence.municipio_db import MunicipioDB


class DBMunicipioRepository(MunicipioRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, municipio: Municipio) -> MunicipioSalida:
        db_municipio = MunicipioDB(**municipio.model_dump())
        self.db.add(db_municipio)
        self.db.commit()
        self.db.refresh(db_municipio)
        return MunicipioSalida.model_validate(db_municipio)

    def buscar_por_id(self, municipio_id: int) -> MunicipioSalida | None:
        db_municipio = self.db.get(MunicipioDB, municipio_id)
        return MunicipioSalida.model_validate(db_municipio) if db_municipio else None

    def listar_municipios(self) -> list[MunicipioSalida]:
        municipios_db = self.db.exec(select(MunicipioDB)).all()
        return [MunicipioSalida.model_validate(m) for m in municipios_db]

def get_municipio_repository(
    session: Session = Depends(get_session),
) -> MunicipioRepository:
    return DBMunicipioRepository(session)