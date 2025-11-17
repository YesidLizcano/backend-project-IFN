from datetime import date

from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository


class EliminarIntegrante:
    """Caso de uso para eliminar un integrante.

    Reglas:
    - Debe existir el integrante.
    - Si tiene asignación a una brigada con fecha de inicio futura
      (mayor a hoy), se bloquea la eliminación.
    """

    def __init__(self, integrante_repository: IntegranteRepository) -> None:
        self.integrante_repository = integrante_repository

    def execute(self, integrante_id: int) -> None:
        """Elimina al integrante si no tiene asignaciones futuras.

        Lanza ValueError con mensaje apropiado en caso de bloqueo o inexistencia.
        """
        existente = self.integrante_repository.buscar_por_id(integrante_id)
        if existente is None:
            raise ValueError("Integrante no encontrado")

        # Nueva regla: solo se puede eliminar si NUNCA ha sido asignado
        if self.integrante_repository.ha_sido_asignado(integrante_id):
            raise ValueError(
                "No se puede eliminar: el integrante ya ha sido asignado a alguna brigada"
            )

        self.integrante_repository.eliminar(integrante_id)
