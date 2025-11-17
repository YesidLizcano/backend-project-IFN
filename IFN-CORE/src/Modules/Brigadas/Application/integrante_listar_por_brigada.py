from typing import List
from src.Modules.Brigadas.Domain.integrante import IntegranteSalida
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository


class IntegranteListarPorBrigada:
    """
    Caso de uso para listar integrantes por brigada.
    """
    def __init__(self, integrante_repository: IntegranteRepository):
        self.integrante_repository = integrante_repository

    def execute(self, brigada_id: int) -> List[IntegranteSalida]:
        """
        Lista todos los integrantes asociados a una brigada.

        Args:
            brigada_id: ID de la brigada
        Returns:
            List[IntegranteSalida]: Lista de integrantes asociados
        """
        return self.integrante_repository.listar_por_brigada(brigada_id)
