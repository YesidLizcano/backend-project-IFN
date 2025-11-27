from datetime import date
from fastapi import Depends
from sqlmodel import Session, select, func, col
from src.Modules.MaterialEquipo.Domain.controlEquipo import ControlEquipo, ControlEquipoGuardar
from src.Modules.MaterialEquipo.Domain.controlEquipo_repository import ControlEquipoRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.controlEquipo_db import ControlEquipoDB
from src.Modules.MaterialEquipo.Infrastructure.Persistence.materialEquipo_db import MaterialEquipoDB
from src.Modules.Ubicacion.Infrastructure.Persistence.departamento_db import DepartamentoDB
from src.Modules.Ubicacion.Infrastructure.Persistence.municipio_db import MunicipioDB
from src.Modules.Brigadas.Infrastructure.Persistence.brigada_db import BrigadaDB
from src.Modules.Conglomerados.Infrastructure.Persistence.conglomerado_db import ConglomeradoDB
from src.Shared.database import get_session


class DBControlEquipoRepository(ControlEquipoRepository):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, control_equipo: ControlEquipoGuardar) -> ControlEquipo:
        db_control_equipo = ControlEquipoDB(**control_equipo.model_dump())
        self.db.add(db_control_equipo)
        self.db.commit()
        self.db.refresh(db_control_equipo)
        return ControlEquipo.model_validate(db_control_equipo)
    
    def buscar_por_id(self, control_equipo_id: int) -> ControlEquipo | None:
        db_control_equipo = self.db.get(ControlEquipoDB, control_equipo_id)
        return ControlEquipo.model_validate(db_control_equipo) if db_control_equipo else None
    
    def calcular_disponibilidad(
        self, 
        nombre_equipo: str, 
        brigada_id: int,
        fecha_inicio: str
    ) -> int:
        """
        Calcula la disponibilidad de un equipo en la fecha de inicio solicitada.
        La disponibilidad depende del periodo del conglomerado asociado a la brigada.
        Se suman las cantidades asignadas en brigadas cuyos conglomerados cubran la fecha_inicio.
        """
        
        # Subconsulta para obtener el departamento_id de la brigada
        departamento_subquery = (
            select(MunicipioDB.departamento_id)
            .select_from(BrigadaDB)
            .join(ConglomeradoDB, BrigadaDB.conglomerado_id == ConglomeradoDB.id)
            .join(MunicipioDB, ConglomeradoDB.municipio_id == MunicipioDB.id)
            .where(BrigadaDB.id == brigada_id)
            .scalar_subquery()
        )
        
        # Subconsulta para calcular el stock ocupado en la fecha de inicio
        # Se hace JOIN con BrigadaDB y ConglomeradoDB para filtrar por fechas del conglomerado
        stock_ocupado = (
            select(func.coalesce(func.sum(ControlEquipoDB.cantidad_asignada), 0))
            .select_from(ControlEquipoDB)
            .join(BrigadaDB, ControlEquipoDB.id_brigada == BrigadaDB.id)
            .join(ConglomeradoDB, BrigadaDB.conglomerado_id == ConglomeradoDB.id)
            .where(
                ControlEquipoDB.id_material_equipo == MaterialEquipoDB.id,
                ConglomeradoDB.fechaInicio <= fecha_inicio,
                ConglomeradoDB.fechaFinAprox >= fecha_inicio
            )
            .correlate(MaterialEquipoDB)
            .scalar_subquery()
        )
        
        # Consulta principal
        query = (
            select(MaterialEquipoDB.cantidad - stock_ocupado)
            .select_from(MaterialEquipoDB)
            .where(
                MaterialEquipoDB.nombre == nombre_equipo,
                MaterialEquipoDB.departamento_id == departamento_subquery
            )
        )
        
        result = self.db.exec(query).first()
        return result if result is not None else 0

    def calcular_disponibilidad_por_nombre_departamento(
        self, 
        nombre_equipo: str, 
        nombre_departamento: str,
        fecha_inicio: str
    ) -> int:
        """
        Calcula la disponibilidad de un equipo en un departamento específico (por nombre) y fecha.
        """
        # Subconsulta para calcular el stock ocupado en la fecha de inicio
        stock_ocupado = (
            select(func.coalesce(func.sum(ControlEquipoDB.cantidad_asignada), 0))
            .select_from(ControlEquipoDB)
            .join(BrigadaDB, ControlEquipoDB.id_brigada == BrigadaDB.id)
            .join(ConglomeradoDB, BrigadaDB.conglomerado_id == ConglomeradoDB.id)
            .where(
                ControlEquipoDB.id_material_equipo == MaterialEquipoDB.id,
                ConglomeradoDB.fechaInicio <= fecha_inicio,
                ConglomeradoDB.fechaFinAprox >= fecha_inicio
            )
            .correlate(MaterialEquipoDB)
            .scalar_subquery()
        )
        
        # Consulta principal con JOIN a DepartamentoDB
        query = (
            select(MaterialEquipoDB.cantidad - stock_ocupado)
            .select_from(MaterialEquipoDB)
            .join(DepartamentoDB, MaterialEquipoDB.departamento_id == DepartamentoDB.id)
            .where(
                MaterialEquipoDB.nombre == nombre_equipo,
                DepartamentoDB.nombre == nombre_departamento
            )
        )
        
        result = self.db.exec(query).first()
        return result if result is not None else 0

    def contar_asignado_desde_hoy(self, id_material_equipo: int) -> int:
        """
        Suma la cantidad asignada para un material cuando hoy está dentro del rango
        del conglomerado asociado a la brigada.
        """
        hoy = date.today()
        query = (
            select(func.coalesce(func.sum(ControlEquipoDB.cantidad_asignada), 0))
            .select_from(ControlEquipoDB)
            .join(BrigadaDB, ControlEquipoDB.id_brigada == BrigadaDB.id)
            .join(ConglomeradoDB, BrigadaDB.conglomerado_id == ConglomeradoDB.id)
            .where(
                ControlEquipoDB.id_material_equipo == id_material_equipo,
                ConglomeradoDB.fechaInicio <= hoy,
                ConglomeradoDB.fechaFinAprox >= hoy,
            )
        )
        result = self.db.exec(query).first()
        return int(result or 0)


def get_control_equipo_repository(
    session: Session = Depends(get_session),
) -> ControlEquipoRepository:
    return DBControlEquipoRepository(session)
