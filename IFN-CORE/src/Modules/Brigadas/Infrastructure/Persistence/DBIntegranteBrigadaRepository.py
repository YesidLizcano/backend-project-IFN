from fastapi import Depends
from sqlmodel import Session
from src.Modules.Brigadas.Domain.integranteBrigada import IntegranteBrigada, IntegranteBrigadaCrear
from src.Modules.Brigadas.Domain.integranteBrigada_repository import IntegranteBrigadaRepository
from src.Modules.Brigadas.Infrastructure.Persistence.integranteBrigada_db import IntegranteBrigadaDB
from src.Shared.Infrastructure.Persistence.database import get_session


class DBIntegranteBrigadaRepository(IntegranteBrigadaRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, integrante_brigada: IntegranteBrigadaCrear) -> IntegranteBrigada:
        db_integrante_brigada = IntegranteBrigadaDB(**integrante_brigada.model_dump())
        self.db.add(db_integrante_brigada)
        self.db.commit()
        self.db.refresh(db_integrante_brigada)
        return IntegranteBrigada.model_validate(db_integrante_brigada)

def get_integrante_brigada_repository(
    session: Session = Depends(get_session),
) -> IntegranteBrigadaRepository:
    return DBIntegranteBrigadaRepository(session)