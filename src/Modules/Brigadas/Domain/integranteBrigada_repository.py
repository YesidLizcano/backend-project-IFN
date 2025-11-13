from abc import ABC, abstractmethod

from src.Modules.Brigadas.Domain.integranteBrigada import IntegranteBrigada, IntegranteBrigadaCrear

class IntegranteBrigadaRepository(ABC):
    @abstractmethod
    def guardar(self, integrante_brigada: IntegranteBrigadaCrear) -> IntegranteBrigada:
        """Persist a integranteBrigada and return the saved domain entity."""
        pass