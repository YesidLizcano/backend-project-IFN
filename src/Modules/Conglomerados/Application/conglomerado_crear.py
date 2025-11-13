from src.Modules.Conglomerados.Domain.conglomerado import Conglomerado, ConglomeradoCrear, ConglomeradoSalida
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Domain.subparcela import Subparcela
from src.Shared.Domain.municipio_repository import MunicipioRepository

from geopy.distance import distance
from geopy import Point


class CrearConglomerado:
    def __init__(
        self,
        conglomerado_repository: ConglomeradoRepository,
        municipio_repository: MunicipioRepository,
    ):
        self.conglomerado_repository = conglomerado_repository
        self.municipio_repository = municipio_repository

    def execute(self, conglomerado: ConglomeradoCrear, municipio_id: int) -> ConglomeradoSalida:
        if not self.municipio_repository.buscar_por_id(municipio_id):
            raise ValueError("Municipio no encontrado")

        conglomerado_salida = Conglomerado(
            **conglomerado.model_dump(),  # Datos del body
            municipio_id=municipio_id # Asigna el ID de la URL
        )
        origen = Point(conglomerado_salida.latitud, conglomerado_salida.longitud)
        azimuts = [0, 90, 180, 270]  # N, E, S, W
        subparcelas = []

        for azimut in azimuts:
            punto = distance(meters=80).destination(origen, azimut)
            subparcelas.append(
                Subparcela(
                    latitud=punto.latitude,
                    longitud=punto.longitude
                )
            )

        return self.conglomerado_repository.guardar(conglomerado_salida, subparcelas)