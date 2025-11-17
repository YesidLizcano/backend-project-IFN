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

    @abstractmethod
    def buscar_por_conglomerado_id(self, conglomerado_id: int) -> BrigadaSalida | None:
        """Buscar una brigada por el `conglomerado_id` asociado (1:1)."""
        pass

    @abstractmethod
    def verificar_minimos(self, brigada_id: int) -> dict:
        """Verificar que la brigada cumpla los mínimos de roles requeridos."""
        pass

    @abstractmethod
    def eliminar(self, brigada_id: int) -> None:
        """Elimina una brigada existente por su identificador."""
        pass

    # @abstractmethod
    # def listar_brigadas(self) -> list[BrigadaSalida]:
    #     """List all brigadas and return them as a list."""
    #     pass