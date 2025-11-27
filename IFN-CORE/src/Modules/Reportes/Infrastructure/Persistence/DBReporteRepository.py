from typing import List, Dict, Any
from sqlmodel import Session, select
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.materialEquipo_db import MaterialEquipoDB
from src.Modules.Ubicacion.Infrastructure.Persistence.departamento_db import DepartamentoDB
from src.Shared.database import get_session
from fastapi import Depends

class DBReporteRepository(ReporteRepository):
    def __init__(self, session: Session):
        self.session = session

    def generar_reporte_inventario(self, nombre_departamento: str) -> List[Dict[str, Any]]:
        query = (
            select(MaterialEquipoDB)
            .join(DepartamentoDB)
            .where(DepartamentoDB.nombre == nombre_departamento)
        )
        resultados = self.session.exec(query).all()
        
        return [
            {
                "id": item.id,
                "nombre": item.nombre,
                "cantidad": item.cantidad,
                "departamento": nombre_departamento
            }
            for item in resultados
        ]

def get_reporte_repository(session: Session = Depends(get_session)) -> ReporteRepository:
    return DBReporteRepository(session)
