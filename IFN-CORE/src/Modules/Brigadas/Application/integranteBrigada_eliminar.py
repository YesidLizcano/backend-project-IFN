from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Domain.integranteBrigada_repository import IntegranteBrigadaRepository


class EliminarIntegranteBrigada:
    """Caso de uso para eliminar un integrante de una brigada verificando mínimos."""

    def __init__(
        self,
        integrante_brigada_repository: IntegranteBrigadaRepository,
        brigada_repository: BrigadaRepository,
    ) -> None:
        self.integrante_brigada_repository = integrante_brigada_repository
        self.brigada_repository = brigada_repository

    def execute(self, brigada_id: int, integrante_id: int) -> None:
        """Elimina la relación Integrante-Brigada respetando los mínimos por rol."""
        relacion = self.integrante_brigada_repository.obtener(brigada_id, integrante_id)
        if relacion is None:
            raise ValueError("La relación Integrante-Brigada no existe")

        info_minimos = self.brigada_repository.verificar_minimos(brigada_id)
        conteos = info_minimos.get("conteos", {})
        requeridos = info_minimos.get("requeridos", {})
        rol = relacion.rol

        if rol in requeridos:
            restante = conteos.get(rol, 0) - 1
            if restante < requeridos[rol]:
                raise ValueError(
                    "No se puede eliminar: se incumplen los mínimos para el rol "
                    f"{rol}."
                )

        self.integrante_brigada_repository.eliminar(brigada_id, integrante_id)
