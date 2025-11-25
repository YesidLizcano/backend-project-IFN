from typing import List
from src.Modules.Brigadas.Domain.integranteBrigada import IntegranteBrigadaRolSalida
from src.Modules.Brigadas.Domain.integranteBrigada_repository import IntegranteBrigadaRepository


class IntegranteListarPorBrigada:
    """
    Caso de uso para listar integrantes por brigada.
    """
    def __init__(self, integrante_brigada_repository: IntegranteBrigadaRepository):
        self.integrante_brigada_repository = integrante_brigada_repository

    def execute(self, brigada_id: int) -> List[IntegranteBrigadaRolSalida]:
        """
        Lista las asignaciones de integrantes y el rol que cumplen en la brigada.

        Args:
            brigada_id: ID de la brigada
        Returns:
            List[IntegranteBrigadaRolSalida]: Lista de roles con datos básicos de integrantes
        """
        return self.integrante_brigada_repository.listar_por_brigada(brigada_id)
