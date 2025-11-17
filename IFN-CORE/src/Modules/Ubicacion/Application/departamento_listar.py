from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository

class ListarDepartamentos:
    def __init__(self, departamento_repository: DepartamentoRepository):
        self.departamento_repository = departamento_repository

    def execute(self):
        return self.departamento_repository.listar_departamentos()
