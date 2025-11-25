from datetime import date

from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Domain.subparcela_repository import SubparcelaRepository


class EliminarConglomerado:
    """Caso de uso para eliminar un conglomerado y sus subparcelas."""

    def __init__(
        self,
        conglomerado_repository: ConglomeradoRepository,
        brigada_repository: BrigadaRepository,
        subparcela_repository: SubparcelaRepository,
    ) -> None:
        self.conglomerado_repository = conglomerado_repository
        self.brigada_repository = brigada_repository
        self.subparcela_repository = subparcela_repository

    def execute(self, conglomerado_id: int) -> dict:
        """Elimina el conglomerado únicamente si la fecha de inicio aún no llega."""
        conglomerado = self.conglomerado_repository.buscar_por_id(conglomerado_id)
        if conglomerado is None:
            raise ValueError("Conglomerado no encontrado")

        fecha_inicio = getattr(conglomerado, "fechaInicio", None)
        if fecha_inicio and fecha_inicio <= date.today():
            raise ValueError(
                "No se puede eliminar el conglomerado: la fecha de inicio ya pasó o es hoy."
            )

        brigada = self.brigada_repository.buscar_por_conglomerado_id(conglomerado_id)
        if brigada is not None:
            self.brigada_repository.eliminar(brigada.id)

        subparcelas_eliminadas = self.subparcela_repository.eliminar_por_conglomerado(
            conglomerado_id
        )
        self.conglomerado_repository.eliminar(conglomerado_id)
        return {
            "conglomerado_id": conglomerado_id,
            "subparcelas_eliminadas": subparcelas_eliminadas,
        }
