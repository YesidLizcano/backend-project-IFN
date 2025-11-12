from sqlmodel import Session

from src.Modules.Conglomerados.Domain.subparcela import Subparcela, SubparcelaSalida
from src.Modules.Conglomerados.Domain.subparcela_repository import SubparcelaRepository
from src.Modules.Conglomerados.Infrastructure.persistence.subparcela_db import SubparcelaDB


class SQLAlchemySubparcelaRepository(SubparcelaRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, subparcela: Subparcela) -> SubparcelaSalida:
        db_subparcela = SubparcelaDB(**subparcela.model_dump())
        self.db.add(db_subparcela)
        self.db.commit()
        self.db.refresh(db_subparcela)
        return SubparcelaSalida.model_validate(db_subparcela)