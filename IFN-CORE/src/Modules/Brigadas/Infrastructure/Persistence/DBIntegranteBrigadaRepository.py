from fastapi import Depends
from sqlmodel import Session, delete, select
from src.Modules.Brigadas.Domain.integranteBrigada import IntegranteBrigada
from src.Modules.Brigadas.Domain.integranteBrigada_repository import IntegranteBrigadaRepository
from src.Modules.Brigadas.Infrastructure.Persistence.integranteBrigada_db import IntegranteBrigadaDB
from src.Shared.database import get_session


class DBIntegranteBrigadaRepository(IntegranteBrigadaRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(
        self,
        integrante_brigada: IntegranteBrigada,
        *,
        commit: bool = True,
    ) -> IntegranteBrigada:
        db_integrante_brigada = IntegranteBrigadaDB(**integrante_brigada.model_dump())
        self.db.add(db_integrante_brigada)
        self.db.flush()
        if commit:
            self.db.commit()
        self.db.refresh(db_integrante_brigada)
        return IntegranteBrigada.model_validate(db_integrante_brigada)

    def obtener(self, brigada_id: int, integrante_id: int) -> IntegranteBrigada | None:
        registro = self.db.get(
            IntegranteBrigadaDB,
            (brigada_id, integrante_id),
        )
        return IntegranteBrigada.model_validate(registro) if registro else None

    def eliminar(
        self,
        id_brigada: int,
        id_integrante: int
    ) -> None:
        self.db.exec(
            delete(IntegranteBrigadaDB).where(
                IntegranteBrigadaDB.id_brigada == id_brigada,
                IntegranteBrigadaDB.id_integrante == id_integrante,
            )
        )
        self.db.commit()

    def listar_por_brigada(self, brigada_id: int) -> list[IntegranteBrigada]:
        registros = self.db.exec(
            select(IntegranteBrigadaDB).where(IntegranteBrigadaDB.id_brigada == brigada_id)
        ).all()
        return [IntegranteBrigada.model_validate(r) for r in registros]
        

def get_integrante_brigada_repository(
    session: Session = Depends(get_session),
) -> IntegranteBrigadaRepository:
    return DBIntegranteBrigadaRepository(session)