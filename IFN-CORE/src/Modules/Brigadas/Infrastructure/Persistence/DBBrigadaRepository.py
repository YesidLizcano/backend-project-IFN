from fastapi import Depends
from sqlmodel import Session
from src.Modules.Brigadas.Domain.brigada import Brigada, BrigadaSalida
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Infrastructure.Persistence.brigada_db import BrigadaDB
from src.Shared.Infrastructure.Persistence.database import get_session


class DBBrigadaRepository(BrigadaRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, brigada: Brigada) -> BrigadaSalida:
        db_brigada = BrigadaDB(**brigada.model_dump())
        self.db.add(db_brigada)
        self.db.commit()
        self.db.refresh(db_brigada)
        return BrigadaSalida.model_validate(db_brigada)
    
    def buscar_por_id(self, brigada_id: int) -> BrigadaSalida | None:
        db_brigada = self.db.get(BrigadaDB, brigada_id)
        return BrigadaSalida.model_validate(db_brigada) if db_brigada else None
    
def get_brigada_repository(
    session: Session = Depends(get_session),
) -> BrigadaRepository:
    return DBBrigadaRepository(session)