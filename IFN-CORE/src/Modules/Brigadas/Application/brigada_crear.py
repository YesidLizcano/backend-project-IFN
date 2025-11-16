from src.Modules.Brigadas.Domain.brigada import Brigada, BrigadaCrear, BrigadaSalida
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository


class CrearBrigada:
    def __init__(
        self,
        brigada_repository: BrigadaRepository,
        conglomerado_repository: ConglomeradoRepository,
    ):
        self.brigada_repository = brigada_repository
        self.conglomerado_repository = conglomerado_repository



    def execute(self, brigada: BrigadaCrear, conglomerado_id: int) -> BrigadaSalida:
        if not self.conglomerado_repository.buscar_por_id(conglomerado_id):
            raise ValueError("Conglomerado no encontrado")
        brigada_salida = Brigada(
            **brigada.model_dump(),  # Datos del body
            conglomerado_id=conglomerado_id # Asigna el ID de la URL
        )

        return self.brigada_repository.guardar(brigada_salida)