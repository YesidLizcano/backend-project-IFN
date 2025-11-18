"""
Caso de uso para listar municipios.

Sigue el patrón de la capa de Aplicación: orquestrar la lógica
de negocio delegando el acceso a datos al repositorio de dominio.
"""

from typing import List

from src.Modules.Ubicacion.Domain.municipio import MunicipioSalida
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository


class ListarMunicipios:
    """
    Caso de uso para obtener todos los municipios.

    Parameters:
    - repository: Implementación de `MunicipioRepository` para acceder a datos.
    """

    def __init__(self, repository: MunicipioRepository) -> None:
        self.repository = repository

    def execute(self) -> List[MunicipioSalida]:
        """
        Retorna el listado completo de municipios.

        Returns:
        - Lista de `MunicipioSalida`.
        """
        return self.repository.listar_municipios()
