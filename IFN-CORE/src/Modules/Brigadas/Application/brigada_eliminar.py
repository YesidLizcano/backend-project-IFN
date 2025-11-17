from datetime import date

from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Conglomerados.Domain.conglomerado_repository import (
    ConglomeradoRepository,
)


class EliminarBrigada:
    """Caso de uso para eliminar una brigada existente."""

    def __init__(
        self,
        brigada_repository: BrigadaRepository,
        conglomerado_repository: ConglomeradoRepository,
    ) -> None:
        self.brigada_repository = brigada_repository
        self.conglomerado_repository = conglomerado_repository

    def execute(self, brigada_id: int) -> None:
        """Valida el conglomerado asociado y elimina la brigada si aún no inicia."""
        brigada = self.brigada_repository.buscar_por_id(brigada_id)
        if brigada is None:
            raise ValueError("Brigada no encontrada")

        conglomerado = self.conglomerado_repository.buscar_por_id(
            brigada.conglomerado_id
        )
        if conglomerado is None:
            raise ValueError("Conglomerado asociado no encontrado")

        if conglomerado.fechaInicio <= date.today():
            raise ValueError(
                "No se puede eliminar la brigada: el conglomerado ya inició "
                f"el {conglomerado.fechaInicio.isoformat()}"
            )

        self.conglomerado_repository.actualizar_fechas(
            conglomerado_id=conglomerado.id,
            fecha_inicio=None,
            fecha_fin_aprox=None,
        )
        self.brigada_repository.eliminar(brigada_id)
