from abc import ABC, abstractmethod

from src.Modules.MaterialEquipo.Domain.materialEquipo import (
    MaterialEquipoCrear,
    MaterialEquipoSalida,
    MaterialEquipoActualizar,
)

class MaterialEquipoRepository(ABC):
    @abstractmethod
    def guardar(self, material_equipo: MaterialEquipoCrear) -> MaterialEquipoSalida:
        """Persist a material_equipo and return the saved domain entity."""
        pass

    @abstractmethod
    def buscar_por_id(self, material_equipo_id: int) -> MaterialEquipoSalida | None:
        """Buscar un material_equipo por su ID. Retorna None si no se encuentra."""
        pass

    @abstractmethod
    def actualizar(
        self, material_equipo_id: int, cambios: MaterialEquipoActualizar
    ) -> MaterialEquipoSalida:
        """Actualizar parcialmente un material_equipo y devolver el DTO actualizado."""
        pass

    @abstractmethod
    def eliminar(self, material_equipo_id: int) -> None:
        """Eliminar un material_equipo existente por su identificador."""
        pass

    @abstractmethod
    def buscar_por_nombre_y_departamento(
        self, nombre: str, departamento_id: int
    ) -> MaterialEquipoSalida | None:
        """Buscar un material/equipo por su nombre y departamento."""
        pass

    @abstractmethod
    def listar_materiales_equipo(self, departamento_id: int) -> list[MaterialEquipoSalida]:
        """Listar materiales/equipos por `departamento_id`.

        Parameters:
        departamento_id (int): Identificador del departamento para filtrar.

        Returns:
        list[MaterialEquipoSalida]: Lista de materiales/equipos del departamento.
        """
        pass