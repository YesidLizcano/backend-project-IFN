"""
Caso de uso para listar Materiales/Equipos por departamento.

Sigue el patrón de Application Layer del proyecto y delega la
obtención de datos al `MaterialEquipoRepository`.
"""

from typing import List

from src.Modules.MaterialEquipo.Domain.materialEquipo import (
    MaterialEquipoSalida,
)
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import (
    MaterialEquipoRepository,
)


class ListarMaterialesEquipo:
    """
    Caso de uso para listar materiales/equipos filtrados por departamento.

    Parameters:
    - repository: Implementación de `MaterialEquipoRepository` utilizada para
      acceder a la capa de persistencia.
    """

    def __init__(self, repository: MaterialEquipoRepository) -> None:
        self.repository = repository

    def execute(self, departamento_id: int) -> List[MaterialEquipoSalida]:
        """
        Retorna los materiales/equipos del departamento indicado.

        Parameters:
        - departamento_id: ID del departamento para filtrar resultados.

        Returns:
        - Lista de `MaterialEquipoSalida`.
        """
        return self.repository.listar_materiales_equipo(departamento_id)
