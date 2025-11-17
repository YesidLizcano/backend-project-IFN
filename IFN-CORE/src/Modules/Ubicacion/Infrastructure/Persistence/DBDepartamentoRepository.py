from fastapi import Depends
from sqlmodel import Session, select
from src.Modules.Ubicacion.Domain.departamento import Departamento, DepartamentoSalida
from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository
from src.Shared.database import get_session
from src.Modules.Ubicacion.Infrastructure.Persistence.departamento_db import DepartamentoDB


class DBDepartamentoRepository(DepartamentoRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, departamento: Departamento) -> DepartamentoSalida:
        db_departamento = DepartamentoDB(**departamento.model_dump())
        self.db.add(db_departamento)
        self.db.commit()
        self.db.refresh(db_departamento)
        return DepartamentoSalida.model_validate(db_departamento)

    def buscar_por_id(self, departamento_id: int) -> DepartamentoSalida | None:
        db_departamento = self.db.get(DepartamentoDB, departamento_id)
        return DepartamentoSalida.model_validate(db_departamento) if db_departamento else None

    def listar_departamentos(self) -> list[DepartamentoSalida]:
        return self.db.exec(select(DepartamentoDB)).all()


def get_departamento_repository(
    session: Session = Depends(get_session),
) -> DepartamentoRepository:
    return DBDepartamentoRepository(session)