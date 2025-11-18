from src.Modules.Ubicacion.Domain.departamento import Departamento, DepartamentoSalida
from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository


class CrearDepartamento:
    def __init__(
        self,
        departamento_repository: DepartamentoRepository,
    ):
        self.departamento_repository = departamento_repository

    def execute(self, departamento: Departamento) -> DepartamentoSalida:
        return self.departamento_repository.guardar(departamento)