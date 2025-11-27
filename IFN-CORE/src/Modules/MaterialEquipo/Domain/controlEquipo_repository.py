from abc import ABC, abstractmethod
from typing import Optional

from src.Modules.MaterialEquipo.Domain.controlEquipo import ControlEquipo, ControlEquipoGuardar


class ControlEquipoRepository(ABC):
    @abstractmethod
    def guardar(self, control_equipo: ControlEquipoGuardar) -> ControlEquipo:
        """Persist a controlEquipo and return the saved domain entity."""
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: int) -> ControlEquipo | None:
        """Find a controlEquipo by its ID."""
        pass
    
    @abstractmethod
    def calcular_disponibilidad(
        self, 
        nombre_equipo: str, 
        brigada_id: int,
        fecha_inicio: str
    ) -> int:
        """
        Calcula la disponibilidad de un equipo en la fecha de inicio solicitada.
        Solo considera asignaciones que estén activas en esa fecha específica.
        """
        pass

    @abstractmethod
    def calcular_disponibilidad_por_nombre_departamento(
        self, 
        nombre_equipo: str, 
        nombre_departamento: str,
        fecha_inicio: str
    ) -> int:
        """
        Calcula la disponibilidad de un equipo en un departamento específico (por nombre) y fecha.
        """
        pass

    @abstractmethod
    def contar_asignado_desde_hoy(self, id_material_equipo: int) -> int:
        """
        Retorna la cantidad total actualmente asignada del material indicado,
        considerando la fecha de hoy dentro del rango de asignación.

        Se suman los registros en ControlEquipoDB donde:
        - ControlEquipoDB.id_material_equipo == id_material_equipo
        - fecha_Inicio_Asignacion <= hoy
        - fecha_Fin_Asignacion es NULL o fecha_Fin_Asignacion >= hoy
        """
        pass
