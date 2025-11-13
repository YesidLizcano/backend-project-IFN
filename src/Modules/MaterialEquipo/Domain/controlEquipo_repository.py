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
