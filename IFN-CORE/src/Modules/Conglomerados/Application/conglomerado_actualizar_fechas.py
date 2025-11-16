from src.Modules.Conglomerados.Domain.conglomerado import ConglomeradoActualizarFechas, ConglomeradoSalida
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository


class ActualizarFechasConglomerado:
    """
    Caso de uso para actualizar las fechas (fechaInicio y fechaFinAprox) 
    de un conglomerado existente.
    """
    
    def __init__(self, conglomerado_repository: ConglomeradoRepository):
        self.conglomerado_repository = conglomerado_repository
    
    def execute(self, conglomerado_id: int, fechas_data: ConglomeradoActualizarFechas) -> ConglomeradoSalida:
        """
        Ejecuta la actualización de fechas para un conglomerado.
        
        Args:
            conglomerado_id: ID del conglomerado a actualizar
            fechas_data: Nuevas fechas (fechaInicio y fechaFinAprox)
            
        Returns:
            ConglomeradoSalida: El conglomerado actualizado
            
        Raises:
            ValueError: Si el conglomerado no existe
        """
        return self.conglomerado_repository.actualizar_fechas(
            conglomerado_id,
            str(fechas_data.fechaInicio),
            str(fechas_data.fechaFinAprox) if fechas_data.fechaFinAprox else None
        )
