from abc import ABC, abstractmethod

from src.Shared.Domain.departamento import Departamento, DepartamentoSalida

class DepartamentoRepository(ABC):
    @abstractmethod
    def guardar(self, departamento: Departamento) -> DepartamentoSalida:
        """Persist a departamento and return the saved domain entity."""
        pass
    
    @abstractmethod
    def buscar_por_id(self, departamento_id: int) -> Departamento | None:
        """Find a departamento by its ID and return the domain entity or None if not found."""
        pass

    @abstractmethod
    def listar_departamentos(self) -> list[Departamento]:
        """List all departamentos and return them as a list."""
        pass