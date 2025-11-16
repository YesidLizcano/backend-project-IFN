from fastapi import Depends
from sqlmodel import Session
from src.Modules.MaterialEquipo.Domain.materialEquipo import MaterialEquipo, MaterialEquipoSalida
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.materialEquipo_db import MaterialEquipoDB
from src.Shared.Infrastructure.Persistence.database import get_session


class DBMaterialEquipoRepository(MaterialEquipoRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, material_equipo: MaterialEquipo) -> MaterialEquipoSalida:
        db_material_equipo = MaterialEquipoDB(**material_equipo.model_dump())
        self.db.add(db_material_equipo)
        self.db.commit()
        self.db.refresh(db_material_equipo)
        return MaterialEquipoSalida.model_validate(db_material_equipo)
    
    def buscar_por_id(self, material_equipo_id: int) -> MaterialEquipoSalida | None:
        db_material_equipo = self.db.get(MaterialEquipoDB, material_equipo_id)
        return MaterialEquipoSalida.model_validate(db_material_equipo) if db_material_equipo else None
    
def get_material_equipo_repository(
    session: Session = Depends(get_session),
) -> MaterialEquipoRepository:
    return DBMaterialEquipoRepository(session)