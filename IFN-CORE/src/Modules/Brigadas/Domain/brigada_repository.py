from abc import ABC, abstractmethod

from src.Modules.Brigadas.Domain.brigada import BrigadaCrear, BrigadaSalida

class BrigadaRepository(ABC):
    @abstractmethod
    def guardar(self, brigada: BrigadaCrear) -> BrigadaSalida:
        """Persist a brigada and return the saved domain entity."""
        pass

    @abstractmethod
    def buscar_por_id(self, brigada_id: int) -> BrigadaSalida | None:
        """Buscar una brigada por su ID. Retorna None si no se encuentra."""
        pass

    # @abstractmethod
    # def listar_brigadas(self) -> list[BrigadaSalida]:
    #     """List all brigadas and return them as a list."""
    #     pass