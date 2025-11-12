from abc import ABC, abstractmethod

from src.Modules.Conglomerados.Domain.subparcela import Subparcela

class SubparcelaRepository(ABC):
    @abstractmethod
    def guardar(self, municipio_id: int, subparcela: Subparcela) -> Subparcela:
        """Persist a subparcela for the given municipio_id and return the saved domain entity."""
        pass

    @abstractmethod
    def buscar_por_id(self, subparcela_id: int) -> Subparcela | None:
        """Buscar una subparcela por su ID. Retorna None si no se encuentra."""
        pass

    @abstractmethod
    def listar_subparcelas(self) -> list[Subparcela]:
        """List all subparcelas and return them as a list."""
        pass