from fastapi import Depends
from sqlmodel import Session
from src.Modules.Brigadas.Domain.integrante import Integrante, IntegranteSalida
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Brigadas.Infrastructure.Persistence.integrante_db import IntegranteDB
from src.Shared.Infrastructure.Persistence.database import get_session


class DBIntegranteRepository(IntegranteRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, integrante: Integrante) -> IntegranteSalida:
        db_integrante = IntegranteDB(**integrante.model_dump())
        self.db.add(db_integrante)
        self.db.commit()
        self.db.refresh(db_integrante)
        return IntegranteSalida.model_validate(db_integrante)
    
    def buscar_por_id(self, integrante_id: int) -> IntegranteSalida | None:
        db_integrante = self.db.get(IntegranteDB, integrante_id)
        return IntegranteSalida.model_validate(db_integrante) if db_integrante else None


def get_integrante_repository(
    session: Session = Depends(get_session),
) -> IntegranteRepository:
    return DBIntegranteRepository(session)