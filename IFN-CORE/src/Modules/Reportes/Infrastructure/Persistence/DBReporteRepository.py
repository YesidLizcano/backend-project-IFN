from typing import List, Dict, Any
from datetime import date
from sqlmodel import Session, select, func
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.materialEquipo_db import MaterialEquipoDB
from src.Modules.MaterialEquipo.Infrastructure.Persistence.controlEquipo_db import ControlEquipoDB
from src.Modules.Ubicacion.Infrastructure.Persistence.departamento_db import DepartamentoDB
from src.Modules.Brigadas.Infrastructure.Persistence.brigada_db import BrigadaDB
from src.Modules.Brigadas.Infrastructure.Persistence.integrante_db import IntegranteDB
from src.Modules.Brigadas.Infrastructure.Persistence.integranteBrigada_db import IntegranteBrigadaDB
from src.Modules.Conglomerados.Infrastructure.Persistence.conglomerado_db import ConglomeradoDB
from src.Modules.Conglomerados.Infrastructure.Persistence.subparcela_db import SubparcelaDB
from src.Shared.database import get_session
from fastapi import Depends

from src.Modules.Ubicacion.Infrastructure.Persistence.municipio_db import MunicipioDB

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

    def generar_reporte_brigadas(self) -> List[Dict[str, Any]]:
        query = (
            select(BrigadaDB, ConglomeradoDB, MunicipioDB)
            .join(ConglomeradoDB, BrigadaDB.conglomerado_id == ConglomeradoDB.id)
            .join(MunicipioDB, ConglomeradoDB.municipio_id == MunicipioDB.id)
        )
        resultados = self.session.exec(query).all()
        
        return [
            {
                "id": brigada.id,
                "fecha_creacion": brigada.fechaCreacion,
                "estado": brigada.estado,
                "conglomerado_id": conglomerado.id,
                "municipio": municipio.nombre,
                "fecha_inicio": conglomerado.fechaInicio,
                "fecha_fin_aprox": conglomerado.fechaFinAprox
            }
            for brigada, conglomerado, municipio in resultados
        ]

    def generar_reporte_conglomerados(self) -> List[Dict[str, Any]]:
        query = (
            select(ConglomeradoDB, MunicipioDB)
            .join(MunicipioDB, ConglomeradoDB.municipio_id == MunicipioDB.id)
        )
        resultados = self.session.exec(query).all()
        
        return [
            {
                "id": conglomerado.id,
                "municipio": municipio.nombre,
                "fecha_inicio": conglomerado.fechaInicio,
                "fecha_fin_aprox": conglomerado.fechaFinAprox,
                "fecha_fin": conglomerado.fechaFin,
                "latitud": conglomerado.latitud,
                "longitud": conglomerado.longitud
            }
            for conglomerado, municipio in resultados
        ]

    def generar_reporte_estadisticas(self) -> Dict[str, int]:
        total_conglomerados = self.session.exec(select(func.count(ConglomeradoDB.id))).one()
        
        total_integrantes_activos = self.session.exec(
            select(func.count(IntegranteDB.id)).where(IntegranteDB.estado == "ACTIVO_DISPONIBLE")
        ).one()
        
        total_brigadas_activas = self.session.exec(
            select(func.count(BrigadaDB.id)).where(BrigadaDB.estado == "ACTIVA")
        ).one()
        
        return {
            "total_conglomerados": total_conglomerados,
            "total_integrantes_activos_disponibles": total_integrantes_activos,
            "total_brigadas_activas": total_brigadas_activas
        }

    def generar_reporte_investigacion(self, conglomerado_id: int) -> Dict[str, Any]:
        # 1. Obtener Conglomerado y Municipio
        conglomerado_query = (
            select(ConglomeradoDB, MunicipioDB)
            .join(MunicipioDB, ConglomeradoDB.municipio_id == MunicipioDB.id)
            .where(ConglomeradoDB.id == conglomerado_id)
        )
        conglomerado_res = self.session.exec(conglomerado_query).first()
        
        if not conglomerado_res:
            return None

        conglomerado, municipio = conglomerado_res
        
        # 2. Obtener Subparcelas
        subparcelas = self.session.exec(
            select(SubparcelaDB).where(SubparcelaDB.conglomerado_id == conglomerado_id)
        ).all()

        # 3. Obtener Brigada
        brigada = self.session.exec(
            select(BrigadaDB).where(BrigadaDB.conglomerado_id == conglomerado_id)
        ).first()

        integrantes_data = []
        materiales_data = []
        brigada_data = None

        if brigada:
            brigada_data = {
                "fecha_creacion": brigada.fechaCreacion,
                "estado": brigada.estado
            }

            # 4. Obtener Integrantes
            integrantes_query = (
                select(IntegranteDB, IntegranteBrigadaDB.rol)
                .join(IntegranteBrigadaDB, IntegranteDB.id == IntegranteBrigadaDB.id_integrante)
                .where(IntegranteBrigadaDB.id_brigada == brigada.id)
            )
            integrantes = self.session.exec(integrantes_query).all()
            integrantes_data = [
                {
                    "nombre": i.nombreCompleto,
                    "rol": rol,
                    "telefono": i.telefono,
                    "email": i.email
                }
                for i, rol in integrantes
            ]

            # 5. Obtener Materiales y Equipos
            materiales_query = (
                select(MaterialEquipoDB, ControlEquipoDB.cantidad_asignada)
                .join(ControlEquipoDB, MaterialEquipoDB.id == ControlEquipoDB.id_material_equipo)
                .where(ControlEquipoDB.id_brigada == brigada.id)
            )
            materiales = self.session.exec(materiales_query).all()
            materiales_data = [
                {
                    "nombre": m.nombre,
                    "cantidad_asignada": cantidad
                }
                for m, cantidad in materiales
            ]

        return {
            "conglomerado": {
                "municipio": municipio.nombre,
                "fecha_inicio": conglomerado.fechaInicio,
                "fecha_fin_aprox": conglomerado.fechaFinAprox,
                "fecha_fin": conglomerado.fechaFin,
                "latitud": conglomerado.latitud,
                "longitud": conglomerado.longitud
            },
            "subparcelas": [
                {"latitud": s.latitud, "longitud": s.longitud} for s in subparcelas
            ],
            "brigada": brigada_data,
            "integrantes": integrantes_data,
            "materiales_equipos": materiales_data
        }

def get_reporte_repository(session: Session = Depends(get_session)) -> ReporteRepository:
    return DBReporteRepository(session)
