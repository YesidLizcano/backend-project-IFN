from fastapi import APIRouter, status, HTTPException
from fastapi import Depends

from src.Modules.Brigadas.Application.integrante_crear import CrearIntegrante
from src.Modules.Brigadas.Domain.integrante import IntegranteCrear, IntegranteSalida
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteRepository import get_integrante_repository
from src.Shared.Domain.municipio_repository import MunicipioRepository
from src.Shared.Infrastructure.Persistence.DBMunicipioRepository import get_municipio_repository


router = APIRouter(tags=["integrantes"])


@router.post(
    "/integrantes/{municipio_id}",
    response_model=IntegranteSalida,
    status_code=status.HTTP_201_CREATED,
)
async def crear_integrante(
    municipio_id: int,
    integrante_data: IntegranteCrear,
    integrante_repo: IntegranteRepository = Depends(get_integrante_repository),
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository)
):
    try:
        creator = CrearIntegrante(integrante_repo, municipio_repo)
        saved_integrante = creator.execute(integrante_data, municipio_id)
        return saved_integrante
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
