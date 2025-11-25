from datetime import date
import json
from src.Modules.Conglomerados.Domain.conglomerado import ConglomeradoActualizarFechas, ConglomeradoSalida
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository


class ActualizarFechasConglomerado:
    """
    Caso de uso para actualizar las fechas (fechaInicio y fechaFinAprox) 
    de un conglomerado existente.
    """
    
    def __init__(
        self,
        conglomerado_repository: ConglomeradoRepository,
        brigada_repository: BrigadaRepository,
        integrante_repository: IntegranteRepository,
    ):
        self.conglomerado_repository = conglomerado_repository
        self.brigada_repository = brigada_repository
        self.integrante_repository = integrante_repository
    
    def execute(self, conglomerado_id: int, fechas_data: ConglomeradoActualizarFechas) -> ConglomeradoSalida:
        """
        Ejecuta la actualización de fechas para un conglomerado.
        
        Args:
            conglomerado_id: ID del conglomerado a actualizar
            fechas_data: Nuevas fechas (fechaInicio y fechaFinAprox)
            
        Returns:
            ConglomeradoSalida: El conglomerado actualizado
            
        Raises:
            ValueError: Si el conglomerado no existe, si la nueva fechaInicio es mayor a fechaFinAprox,
            o si la fechaInicio actual en la BD no es posterior a la fecha de hoy.
        """

        if fechas_data.fechaInicio is None or fechas_data.fechaFinAprox is None:
            raise ValueError("Las fechas fechaInicio y fechaFinAprox no pueden estar vacías")

        # Validación de consistencia: fechaInicio <= fechaFinAprox
        if fechas_data.fechaInicio > fechas_data.fechaFinAprox:
            raise ValueError(
                "La fechaInicio debe ser anterior o igual a la fechaFinAprox"
            )

        # Obtener el conglomerado actual para validar la fecha en BD
        actual = self.conglomerado_repository.buscar_por_id(conglomerado_id)
        if actual is None:
            raise ValueError("El conglomerado especificado no existe")

        # La fechaInicio actual (guardada en BD) debe ser posterior a hoy
        hoy = date.today()
        if not (actual.fechaInicio > hoy):
            raise ValueError("La fechaInicio actual del conglomerado debe ser posterior a la fecha de hoy")
        # Verificar si existe brigada asociada a este conglomerado
        brigada = self.brigada_repository.buscar_por_conglomerado_id(conglomerado_id)
        if brigada is not None:
            # Validar solapamientos de integrantes con el nuevo rango de fechas
            resultado = self.integrante_repository.listar_integrantes_con_y_sin_solapamiento(
                brigada_id=brigada.id,
                fecha_inicio=fechas_data.fechaInicio,
                fecha_fin_aprox=fechas_data.fechaFinAprox,
            )
            conflictos = resultado.get("con_solapamiento", [])
            if conflictos:
                # Incluir integrantes completos tanto con como sin solapamiento
                conflictos_serializados = [c.model_dump() for c in conflictos]
                sin_conf_serializados = [s.model_dump() for s in resultado.get("sin_solapamiento", [])]
                payload = {
                    "tipo": "CONFLICTO_SOLAPAMIENTO",
                    "conglomerado_id": conglomerado_id,
                    "brigada_id": brigada.id,
                    "con_solapamiento": conflictos_serializados,
                    "sin_solapamiento": sin_conf_serializados,
                }
                # Prefijo para que el router lo detecte y responda 409 con detalle estructurado
                raise ValueError("CONFLICTO_SOLAPAMIENTO:" + json.dumps(payload))

        # Si no hay brigada o no hay conflictos, proceder con la actualización
        return self.conglomerado_repository.actualizar_fechas(
            conglomerado_id,
            fechas_data.fechaInicio,
            fechas_data.fechaFinAprox,
        )
