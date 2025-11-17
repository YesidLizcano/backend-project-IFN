from datetime import date

from src.Modules.Brigadas.Domain.integrante import IntegranteActualizar, IntegranteSalida, StatusEnum
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Shared.Domain.municipio_repository import MunicipioRepository


class ActualizarIntegrante:
    """Caso de uso para actualización parcial de Integrante.

    Regla: si se actualiza `estado` a un valor diferente de
    `ACTIVO_DISPONIBLE`, se debe verificar que el integrante NO tenga
    asignaciones futuras usando `tiene_asignacion_futura`.
    """

    def __init__(
        self,
        integrante_repository: IntegranteRepository,
        municipio_repository: MunicipioRepository | None = None,
    ) -> None:
        self.integrante_repository = integrante_repository
        self.municipio_repository = municipio_repository

    def execute(self, integrante_id: int, cambios: IntegranteActualizar) -> IntegranteSalida:
        existente = self.integrante_repository.buscar_por_id(integrante_id)
        if existente is None:
            raise ValueError("Integrante no encontrado")

        datos = cambios.model_dump(exclude_unset=True, exclude_none=True)
        if not datos:
            raise ValueError("Debe proporcionar al menos un campo a actualizar")

        if "estado" in datos:
            # Mapear a StatusEnum aquí (fuera del repositorio)
            try:
                nuevo_estado_enum = StatusEnum(datos["estado"]) if datos["estado"] is not None else None
            except Exception:
                raise ValueError("Estado inválido")

            # Regla de validación según nuevo estado
            if nuevo_estado_enum != StatusEnum.ACTIVO_DISPONIBLE:
                hoy = date.today()
                if self.integrante_repository.tiene_asignacion_futura(integrante_id, hoy):
                    raise ValueError(
                        "No se puede actualizar el estado: el integrante tiene asignaciones futuras"
                    )

            # Actualizar el payload con el Enum mapeado
            cambios = cambios.model_copy(update={"estado": nuevo_estado_enum})

        # Validar municipio si se solicita cambio
        if "municipio_id" in datos and datos["municipio_id"] is not None:
            municipio = self.municipio_repository.buscar_por_id(datos["municipio_id"])
            if municipio is None:
                raise ValueError("Municipio no encontrado")

        return self.integrante_repository.actualizar(integrante_id, cambios)
