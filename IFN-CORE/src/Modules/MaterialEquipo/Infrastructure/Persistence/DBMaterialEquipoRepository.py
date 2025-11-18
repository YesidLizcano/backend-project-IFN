from fastapi import Depends
from sqlmodel import Session, delete, select
from src.Modules.MaterialEquipo.Domain.materialEquipo import (
    MaterialEquipo,
    MaterialEquipoSalida,
    MaterialEquipoActualizar,
)
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.materialEquipo_db import MaterialEquipoDB
from src.Modules.MaterialEquipo.Infrastructure.Persistence.controlEquipo_db import ControlEquipoDB
from src.Shared.database import get_session


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

    def actualizar(
        self, material_equipo_id: int, cambios: MaterialEquipoActualizar
    ) -> MaterialEquipoSalida:
        """Actualiza parcialmente un material_equipo existente."""
        db_material = self.db.get(MaterialEquipoDB, material_equipo_id)
        if db_material is None:
            raise ValueError("Material no encontrado")

        # Aplicar cambios solo si vienen en el payload
        datos = cambios.model_dump(exclude_unset=True)
        if not datos:
            raise ValueError("Debe proporcionar al menos un campo a actualizar")

    # VALIDACIÓN CORRECTA DE CANTIDAD (sumar/restar)
        if "cantidad" in datos:
            nueva_cantidad = db_material.cantidad + datos["cantidad"]
            if nueva_cantidad < 0:
                raise ValueError("La cantidad resultante no puede ser negativa")
            
            datos["cantidad"] = nueva_cantidad

        for campo, valor in datos.items():
            setattr(db_material, campo, valor)

        try:
            self.db.add(db_material)
            self.db.commit()
            self.db.refresh(db_material)
        except Exception:
            self.db.rollback()
            raise

        return MaterialEquipoSalida.model_validate(db_material)

    def eliminar(self, material_equipo_id: int) -> None:
        """Elimina el material/equipo y sus asignaciones de control asociadas."""
        try:
            self.db.exec(
                delete(ControlEquipoDB).where(
                    ControlEquipoDB.id_material_equipo == material_equipo_id
                )
            )
            resultado = self.db.exec(
                delete(MaterialEquipoDB).where(MaterialEquipoDB.id == material_equipo_id)
            )
            if not resultado.rowcount:
                self.db.rollback()
                raise ValueError("Material/Equipo no encontrado")
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def buscar_por_nombre_y_departamento(
        self, nombre: str, departamento_id: int
    ) -> MaterialEquipoSalida | None:
        stmt = (
            select(MaterialEquipoDB)
            .where(MaterialEquipoDB.nombre == nombre)
            .where(MaterialEquipoDB.departamento_id == departamento_id)
        )
        db_item = self.db.exec(stmt).first()
        return MaterialEquipoSalida.model_validate(db_item) if db_item else None

    def listar_materiales_equipo(self, departamento_id: int) -> list[MaterialEquipoSalida]:
        """Lista materiales/equipos filtrando por departamento.

        Parameters:
            departamento_id: ID del departamento para filtrar resultados.

        Returns:
            list[MaterialEquipoSalida]: Materiales/equipos del departamento indicado.
        """
        stmt = select(MaterialEquipoDB).where(
            MaterialEquipoDB.departamento_id == departamento_id
        )
        items = self.db.exec(stmt).all()
        return [MaterialEquipoSalida.model_validate(i) for i in items]
    
def get_material_equipo_repository(
    session: Session = Depends(get_session),
) -> MaterialEquipoRepository:
    return DBMaterialEquipoRepository(session)