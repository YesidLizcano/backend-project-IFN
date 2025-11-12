from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Domain.subparcela import Subparcela
from src.Modules.Conglomerados.Domain.subparcela_repository import SubparcelaRepository


class CrearSubparcela:
    def __init__(
        self,
        subparcela_repository: SubparcelaRepository,
        conglomerado_repository: ConglomeradoRepository,
    ):
        self.subparcela_repository = subparcela_repository
        self.conglomerado_repository = conglomerado_repository

    def execute(self, subparcela: Subparcela) -> Subparcela:
        if not self.conglomerado_repository.buscar_por_id(subparcela.conglomerado_id):
            raise ValueError("Conglomerado no encontrado")
        return self.subparcela_repository.guardar(subparcela)