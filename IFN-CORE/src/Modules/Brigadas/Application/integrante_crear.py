from src.Modules.Brigadas.Domain.integrante import Integrante, IntegranteCrear, IntegranteSalida
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository


class CrearIntegrante:
    def __init__(
        self,
        integrante_repository: IntegranteRepository,
        municipio_repository: MunicipioRepository,
    ):
        self.integrante_repository = integrante_repository
        self.municipio_repository = municipio_repository

    def execute(self, integrante: IntegranteCrear, municipio_id: int) -> IntegranteSalida:
        if not self.municipio_repository.buscar_por_id(municipio_id):
            raise ValueError("Municipio no encontrado")

        integrante_salida = Integrante(
            **integrante.model_dump(),  # Datos del body
            municipio_id=municipio_id # Asigna el ID de la URL
        )

        return self.integrante_repository.guardar(integrante_salida)