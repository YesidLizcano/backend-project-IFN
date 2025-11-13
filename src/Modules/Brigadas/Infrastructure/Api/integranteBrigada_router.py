from fastapi import APIRouter, Depends, status, HTTPException

from src.Modules.Brigadas.Application.integranteBrigada_crear import CrearIntegranteBrigada
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Domain.integranteBrigada import IntegranteBrigada, IntegranteBrigadaCrear
from src.Modules.Brigadas.Domain.integranteBrigada_repository import IntegranteBrigadaRepository
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteBrigadaRepository import get_integrante_brigada_repository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteRepository import get_integrante_repository
from src.Modules.Brigadas.Infrastructure.Persistence.DBBrigadaRepository import get_brigada_repository


router = APIRouter(tags=["integranteBrigada"])


@router.post(
    "/brigadas/{brigada_id}/integrantes/{integrante_id}",
    response_model=IntegranteBrigada,
    status_code=status.HTTP_201_CREATED,
)
async def asignar_integrante_brigada(
    brigada_id: int,
    integrante_id: int,
    integrante_brigada_data: IntegranteBrigadaCrear,
    integrante_brigada_repo: IntegranteBrigadaRepository = Depends(get_integrante_brigada_repository),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    integrante_repo: IntegranteRepository = Depends(get_integrante_repository),
):
    try:
        creator = CrearIntegranteBrigada(integrante_brigada_repo, brigada_repo, integrante_repo)
        saved_brigada = creator.execute(integrante_brigada_data, brigada_id, integrante_id)
        return saved_brigada
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))