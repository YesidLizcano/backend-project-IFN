from abc import ABC, abstractmethod

from src.Modules.Brigadas.Domain.integranteBrigada import IntegranteBrigada

class IntegranteBrigadaRepository(ABC):
    @abstractmethod
    def guardar(
        self,
        integrante_brigada: IntegranteBrigada,
        *,
        commit: bool = True,
    ) -> IntegranteBrigada:
        """Persist a integranteBrigada and return the saved domain entity."""
        pass

    @abstractmethod
    def obtener(self, brigada_id: int, integrante_id: int) -> IntegranteBrigada | None:
        """Obtiene la relación Integrante-Brigada si existe."""
        pass

    @abstractmethod
    def eliminar(
        self,
        relacion: IntegranteBrigada,
    ) -> None:
        """Eliminar la relación Integrante-Brigada utilizando la instancia ya consultada."""
        pass