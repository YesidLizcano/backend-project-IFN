from abc import ABC, abstractmethod

from src.Modules.MaterialEquipo.Domain.materialEquipo import MaterialEquipoCrear, MaterialEquipoSalida

class MaterialEquipoRepository(ABC):
    @abstractmethod
    def guardar(self, material_equipo: MaterialEquipoCrear) -> MaterialEquipoSalida:
        """Persist a material_equipo and return the saved domain entity."""
        pass

    @abstractmethod
    def buscar_por_id(self, material_equipo_id: int) -> MaterialEquipoSalida | None:
        """Buscar un material_equipo por su ID. Retorna None si no se encuentra."""
        pass

    # @abstractmethod
    # def listar_materiales_equipo(self) -> list[MaterialEquipoSalida]:
    #     """List all materiales_equipo and return them as a list."""
    #     pass