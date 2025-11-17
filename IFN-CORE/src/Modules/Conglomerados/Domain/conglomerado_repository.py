from abc import ABC, abstractmethod

from src.Modules.Conglomerados.Domain.conglomerado import ConglomeradoCrear, ConglomeradoSalida
from src.Modules.Conglomerados.Domain.subparcela import Subparcela

class ConglomeradoRepository(ABC):
    @abstractmethod
    def guardar(self, conglomerado: ConglomeradoCrear, subparcelas: list[Subparcela]) -> ConglomeradoSalida:
        """Persist a conglomerado for the given municipio_id and return the saved domain entity."""
        pass

    @abstractmethod
    def buscar_por_id(self, conglomerado_id: int) -> ConglomeradoSalida | None:
        """Buscar un conglomerado por su ID. Retorna None si no se encuentra."""
        pass

    @abstractmethod
    def listar_conglomerados(self) -> list[ConglomeradoSalida]:
        """List all conglomerados and return them as a list."""
        pass

    @abstractmethod
    def actualizar_fechas(
        self,
        conglomerado_id: int,
        fecha_inicio: str | None,
        fecha_fin_aprox: str | None,
    ) -> ConglomeradoSalida:
        """Actualizar o limpiar fechaInicio y fechaFinAprox de un conglomerado."""
        pass

    @abstractmethod
    def eliminar(self, conglomerado_id: int) -> None:
        """Eliminar un conglomerado existente por su identificador."""
        pass