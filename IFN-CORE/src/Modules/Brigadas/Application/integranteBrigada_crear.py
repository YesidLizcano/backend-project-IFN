from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Domain.integranteBrigada import IntegranteBrigada, IntegranteBrigadaCrear
from src.Modules.Brigadas.Domain.integranteBrigada_repository import IntegranteBrigadaRepository
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository


class CrearIntegranteBrigada:
    def __init__(
        self,
        integranteBrigada_repository: IntegranteBrigadaRepository,
        brigada_repository: BrigadaRepository,
        integrante_repository: IntegranteRepository,
    ):
        self.integranteBrigada_repository = integranteBrigada_repository
        self.brigada_repository = brigada_repository
        self.integrante_repository = integrante_repository

    def execute(self, integranteBrigada: IntegranteBrigadaCrear, brigada_id: int, integrante_id: int) -> IntegranteBrigada:
        if not self.brigada_repository.buscar_por_id(brigada_id):
            raise ValueError("Brigada no encontrada")
        if not self.integrante_repository.buscar_por_id(integrante_id):
            raise ValueError("Integrante no encontrado")

        integrante_brigada = IntegranteBrigada(
            **integranteBrigada.model_dump(),  # Datos del body
            id_brigada=brigada_id,
            id_integrante=integrante_id,
        )

        return self.integranteBrigada_repository.guardar(integrante_brigada)