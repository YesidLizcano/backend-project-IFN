from datetime import date
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Domain.conglomerado import ConglomeradoSalida, ConglomeradoFinalizar

class FinalizarConglomerado:
    def __init__(self, conglomerado_repository: ConglomeradoRepository):
        self.conglomerado_repository = conglomerado_repository

    def execute(self, conglomerado_id: int, datos: ConglomeradoFinalizar) -> ConglomeradoSalida:
        conglomerado = self.conglomerado_repository.buscar_por_id(conglomerado_id)
        if not conglomerado:
            raise ValueError(f"Conglomerado con ID {conglomerado_id} no encontrado")
            
        if conglomerado.fechaInicio and datos.fechaFin < conglomerado.fechaInicio:
             raise ValueError("La fecha de finalización no puede ser anterior a la fecha de inicio")

        return self.conglomerado_repository.finalizar(conglomerado_id, datos.fechaFin)
