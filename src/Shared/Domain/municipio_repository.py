from abc import ABC, abstractmethod

from src.Shared.Domain.municipio import Municipio

class MunicipioRepository(ABC):
    @abstractmethod
    def guardar(self, municipio: Municipio) -> Municipio:
        """Persist a municipio and return the saved domain entity."""
        pass

    @abstractmethod
    def buscar_por_id(self, municipio_id: int) -> Municipio | None:
        """Find a municipio by its ID and return the domain entity or None if not found."""
        pass


    def listar_municipios(self) -> list[Municipio]:
        """List all municipios and return them as a list."""
        pass