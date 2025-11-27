from typing import List, Dict, Any
from datetime import date
from sqlmodel import Session, select, func
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.materialEquipo_db import MaterialEquipoDB
from src.Modules.MaterialEquipo.Infrastructure.Persistence.controlEquipo_db import ControlEquipoDB
from src.Modules.Ubicacion.Infrastructure.Persistence.departamento_db import DepartamentoDB
from src.Modules.Brigadas.Infrastructure.Persistence.brigada_db import BrigadaDB
from src.Modules.Conglomerados.Infrastructure.Persistence.conglomerado_db import ConglomeradoDB
from src.Shared.database import get_session
from fastapi import Depends

class DBReporteRepository(ReporteRepository):
    def __init__(self, session: Session):
        self.session = session

    def generar_reporte_inventario(self, nombre_departamento: str) -> List[Dict[str, Any]]:
        hoy = date.today()
        
        # Subconsulta para calcular el stock ocupado hoy
        stock_ocupado_subquery = (
            select(func.coalesce(func.sum(ControlEquipoDB.cantidad_asignada), 0))
            .select_from(ControlEquipoDB)
            .join(BrigadaDB, ControlEquipoDB.id_brigada == BrigadaDB.id)
            .join(ConglomeradoDB, BrigadaDB.conglomerado_id == ConglomeradoDB.id)
            .where(
                ControlEquipoDB.id_material_equipo == MaterialEquipoDB.id,
                ConglomeradoDB.fechaInicio <= hoy,
                ConglomeradoDB.fechaFinAprox >= hoy
            )
            .correlate(MaterialEquipoDB)
            .scalar_subquery()
        )

        query = (
            select(
                MaterialEquipoDB.id,
                MaterialEquipoDB.nombre,
                MaterialEquipoDB.cantidad,
                stock_ocupado_subquery.label("ocupado")
            )
            .join(DepartamentoDB, MaterialEquipoDB.departamento_id == DepartamentoDB.id)
            .where(DepartamentoDB.nombre == nombre_departamento)
        )
        
        resultados = self.session.exec(query).all()
        
        return [
            {
                "id": row.id,
                "nombre": row.nombre,
                "cantidad_total": row.cantidad,
                "cantidad_ocupada": row.ocupado,
                "cantidad_disponible": row.cantidad - row.ocupado,
                "departamento": nombre_departamento
            }
            for row in resultados
        ]

def get_reporte_repository(session: Session = Depends(get_session)) -> ReporteRepository:
    return DBReporteRepository(session)
