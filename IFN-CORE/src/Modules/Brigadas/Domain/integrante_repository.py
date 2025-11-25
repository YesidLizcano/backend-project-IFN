from abc import ABC, abstractmethod
from typing import List
from datetime import date

from src.Modules.Brigadas.Domain.integrante import Integrante, IntegranteSalida, IntegranteActualizar

class IntegranteRepository(ABC):
    @abstractmethod
    def guardar(self, integrante: Integrante) -> IntegranteSalida:
        """Persist an integrante and return the saved domain entity."""
        pass

    @abstractmethod
    def buscar_asignaciones_superpuestas(
        self,
        integrante_id,
        fecha_inicio: date,
        fecha_fin_aprox: date,
        excluir_brigada_id: int | None = None,
    ):
        """Check for overlapping assignments for an integrante within a date range, optionally excluding a specific brigada."""
        pass
    
    @abstractmethod
    def buscar_por_id(self, integrante_id: int) -> IntegranteSalida | None:
        """Find an integrante by its ID."""
        pass
    
    @abstractmethod
    def listar_por_region(self, ids_departamentos: List[int], fecha_inicio: date, fecha_fin_aprox: date) -> List[IntegranteSalida]:
        """Find active integrantes from given departamentos available in [fecha_inicio, fecha_fin_aprox]."""
        pass

    @abstractmethod
    def listar_por_brigada(self, brigada_id: int) -> List[IntegranteSalida]:
        """List all integrantes associated with a specific brigada."""
        pass

    @abstractmethod
    def listar_integrantes_con_y_sin_solapamiento(self, brigada_id: int, fecha_inicio: date, fecha_fin_aprox: date) -> dict:
        """List integrantes partitioned by those with and without overlapping assignments in the given date range."""
        pass

    @abstractmethod
    def tiene_asignacion_futura(self, integrante_id: int, referencia: date) -> bool:
        """Retorna True si el integrante tiene una asignación con fechaInicio > referencia."""
        pass

    @abstractmethod
    def eliminar(self, integrante_id: int) -> None:
        """Elimina un integrante existente por su identificador."""
        pass

    @abstractmethod
    def ha_sido_asignado(self, integrante_id: int) -> bool:
        """
        Retorna True si el integrante tiene, o ha tenido, al menos una
        relación en `IntegranteBrigada` (sin importar fechas).
        """
        pass

    @abstractmethod
    def actualizar(self, integrante_id: int, cambios: IntegranteActualizar) -> IntegranteSalida:
        """Actualiza parcialmente un integrante y devuelve el DTO actualizado."""
        pass