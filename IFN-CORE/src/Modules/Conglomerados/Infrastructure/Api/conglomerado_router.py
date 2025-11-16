from fastapi import APIRouter, HTTPException, status

from fastapi import Depends

from src.Modules.Conglomerados.Domain.conglomerado import (
    Conglomerado, 
    ConglomeradoCrear, 
    ConglomeradoActualizarFechas,
    ConglomeradoSalida
)
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Infrastructure.Persistence.DBConglomeradoRepository import get_conglomerado_repository
from src.Modules.Conglomerados.Application.conglomerado_crear import CrearConglomerado
from src.Modules.Conglomerados.Application.conglomerado_actualizar_fechas import ActualizarFechasConglomerado
from src.Shared.Domain.municipio_repository import MunicipioRepository
from src.Shared.Infrastructure.Persistence.DBMunicipioRepository import (
    get_municipio_repository,
)

router = APIRouter(tags=["conglomerados"])


@router.post(
    "/conglomerados/{municipio_id}",
    response_model=ConglomeradoSalida,
    status_code=status.HTTP_201_CREATED,
)
async def crear_conglomerado(
    municipio_id: int,
    conglomerado_data: ConglomeradoCrear,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository)
):
    try:
        creator = CrearConglomerado(conglomerado_repo, municipio_repo)
        saved_conglomerado = creator.execute(conglomerado_data, municipio_id)
        return saved_conglomerado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch(
    "/conglomerados/{conglomerado_id}/fechas",
    response_model=ConglomeradoSalida,
    status_code=status.HTTP_200_OK,
)
async def actualizar_fechas_conglomerado(
    conglomerado_id: int,
    fechas_data: ConglomeradoActualizarFechas,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository)
):
    """
    Actualiza las fechas (fechaInicio y fechaFinAprox) de un conglomerado existente.
    
    Args:
        conglomerado_id: ID del conglomerado a actualizar
        fechas_data: Nuevas fechas a asignar
    """
    try:
        actualizador = ActualizarFechasConglomerado(conglomerado_repo)
        conglomerado_actualizado = actualizador.execute(conglomerado_id, fechas_data)
        return conglomerado_actualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error al actualizar fechas: {str(e)}"
        )
