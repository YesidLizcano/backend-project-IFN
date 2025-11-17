from fastapi import Depends
from sqlmodel import Session, delete

from src.Modules.Conglomerados.Domain.subparcela import Subparcela, SubparcelaSalida
from src.Modules.Conglomerados.Domain.subparcela_repository import SubparcelaRepository
from src.Modules.Conglomerados.Infrastructure.Persistence.subparcela_db import SubparcelaDB
from src.Shared.Infrastructure.Persistence.database import get_session


class DBSubparcelaRepository(SubparcelaRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, subparcela: Subparcela) -> SubparcelaSalida:
        db_subparcela = SubparcelaDB(**subparcela.model_dump())
        self.db.add(db_subparcela)
        self.db.commit()
        self.db.refresh(db_subparcela)
        return SubparcelaSalida.model_validate(db_subparcela)

    def eliminar_por_conglomerado(self, conglomerado_id: int) -> int:
        """Elimina todas las subparcelas asociadas a un conglomerado y retorna la cantidad afectada."""
        resultado = self.db.exec(
            delete(SubparcelaDB).where(SubparcelaDB.conglomerado_id == conglomerado_id)
        )
        self.db.commit()
        return resultado.rowcount or 0


def get_subparcela_repository(session: Session = Depends(get_session)) -> SubparcelaRepository:
    return DBSubparcelaRepository(session)