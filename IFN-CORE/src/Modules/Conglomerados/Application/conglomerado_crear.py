from src.Modules.Conglomerados.Domain.conglomerado import Conglomerado, ConglomeradoCrear, ConglomeradoSalida
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Domain.subparcela import Subparcela
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository

from geopy.distance import distance
from geopy import Point as GeoPoint
import geopandas as gpd
from shapely.geometry import Point as ShapelyPoint


class CrearConglomerado:
    def __init__(
        self,
        conglomerado_repository: ConglomeradoRepository,
        municipio_repository: MunicipioRepository,
    ):
        self.conglomerado_repository = conglomerado_repository
        self.municipio_repository = municipio_repository
        
        # Cargar solo una vez: Mucho más rápido
        self.colombia = gpd.read_file("colombia.geo.json")

    def conglomerado_en_colombia(self, lon: float, lat: float) -> bool:
        punto = ShapelyPoint(lon, lat)  # shapely usa (lon, lat)
        return self.colombia.contains(punto).any()

    def execute(self, conglomerado: ConglomeradoCrear, municipio_id: int) -> ConglomeradoSalida:
        # Validar municipio
        if not self.municipio_repository.buscar_por_id(municipio_id):
            raise ValueError("Municipio no encontrado")

        # Preparar objeto de salida
        conglomerado_salida = Conglomerado(
            **conglomerado.model_dump(),
            municipio_id=municipio_id
        )

        # Usar geopy para mover las subparcelas
        origen = GeoPoint(conglomerado_salida.latitud, conglomerado_salida.longitud)
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
