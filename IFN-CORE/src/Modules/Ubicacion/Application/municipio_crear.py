from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository
from src.Modules.Ubicacion.Domain.municipio import Municipio, MunicipioCrear, MunicipioSalida
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository


class CrearMunicipio:
    def __init__(
        self,
        municipio_repository: MunicipioRepository,
        departamento_repository: DepartamentoRepository,
    ):
        self.departamento_repository = departamento_repository
        self.municipio_repository = municipio_repository

    def execute(self, municipio_data: MunicipioCrear, departamento_id: int) -> MunicipioSalida:
        # Validar que el departamento existe
        if not self.departamento_repository.buscar_por_id(departamento_id):
            raise ValueError(f"Departamento con ID {departamento_id} no encontrado")
        
        # Crear el municipio completo con el departamento_id
        municipio = Municipio(
            nombre=municipio_data.nombre,
            departamento_id=departamento_id
        )
        
        return self.municipio_repository.guardar(municipio)