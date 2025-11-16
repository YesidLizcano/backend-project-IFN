from abc import ABC, abstractmethod
from typing import List
from datetime import date

from src.Modules.Brigadas.Domain.integrante import Integrante, IntegranteSalida

class IntegranteRepository(ABC):
    @abstractmethod
    def guardar(self, integrante: Integrante) -> IntegranteSalida:
        """Persist an integrante and return the saved domain entity."""
        pass
    
    @abstractmethod
    def buscar_por_id(self, integrante_id: int) -> IntegranteSalida | None:
        """Find an integrante by its ID."""
        pass
    
    @abstractmethod
    def listar_por_region(self, ids_departamentos: List[int], fecha_inicio: date, fecha_fin_aprox: date, rol: str) -> List[IntegranteSalida]:
        """Find active integrantes from given departamentos available in [fecha_inicio, fecha_fin_aprox] with the specified rol."""
        pass

    # @abstractmethod
    # def listar_integrantes(self) -> list[IntegranteSalida]:
    #     """List all integrantes and return them as a list."""
    #     pass