from src.Shared.Domain.departamento_repository import DepartamentoRepository
from src.Shared.Domain.municipio import Municipio
from src.Shared.Domain.municipio_repository import MunicipioRepository


class CrearMunicipio:
    def __init__(
        self,
        municipio_repository: MunicipioRepository,
        departamento_repository: DepartamentoRepository,
    ):
        self.departamento_repository = departamento_repository
        self.municipio_repository = municipio_repository

    def execute(self, municipio: Municipio) -> Municipio:
        if not self.departamento_repository.buscar_por_id(municipio.departamento_id):
            raise ValueError("Departamento no encontrado")
        print(municipio)
        return self.municipio_repository.guardar(municipio)