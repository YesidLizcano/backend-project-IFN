from abc import ABC, abstractmethod

from src.Modules.Brigadas.Domain.integrante import IntegranteCrear, IntegranteSalida

class IntegranteRepository(ABC):
    @abstractmethod
    def guardar(self, integrante: IntegranteCrear) -> IntegranteSalida:
        """Persist a integrante and return the saved domain entity."""
        pass

    @abstractmethod
    def buscar_por_id(self, integrante_id: int) -> IntegranteSalida | None:
        """Buscar un integrante por su ID. Retorna None si no se encuentra."""
        pass

    # @abstractmethod
    # def listar_integrantes(self) -> list[IntegranteSalida]:
    #     """List all integrantes and return them as a list."""
    #     pass