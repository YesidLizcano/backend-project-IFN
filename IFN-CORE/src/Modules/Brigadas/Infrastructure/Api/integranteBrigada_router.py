from fastapi import APIRouter, Depends, status, HTTPException

from src.Modules.Brigadas.Application.integranteBrigada_crear import CrearIntegranteBrigada
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Domain.integranteBrigada import IntegranteBrigada, IntegranteBrigadaCrear
from src.Modules.Brigadas.Domain.integranteBrigada_repository import IntegranteBrigadaRepository
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteBrigadaRepository import get_integrante_brigada_repository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteRepository import get_integrante_repository
from src.Modules.Brigadas.Infrastructure.Persistence.DBBrigadaRepository import get_brigada_repository
from src.Modules.Brigadas.Application.integranteBrigada_eliminar import EliminarIntegranteBrigada
from src.Shared.Auth.Domain.auth_service_interface import TokenPayload
from src.Shared.Auth.Infrastructure.dependencies import get_token_payload


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
    token_payload: TokenPayload = Depends(get_token_payload),
):
    try:
        creator = CrearIntegranteBrigada(integrante_brigada_repo, brigada_repo, integrante_repo)
        saved_brigada = creator.execute(integrante_brigada_data, brigada_id, integrante_id)
        return saved_brigada
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/brigadas/{brigada_id}/integrantes/{integrante_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def eliminar_integrante_de_brigada(
    brigada_id: int,
    integrante_id: int,
    integrante_brigada_repo: IntegranteBrigadaRepository = Depends(get_integrante_brigada_repository),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Elimina la relación Integrante-Brigada cumpliendo los mínimos de roles."""
    try:
        eliminador = EliminarIntegranteBrigada(
            integrante_brigada_repository=integrante_brigada_repo,
            brigada_repository=brigada_repo,
        )
        eliminador.execute(brigada_id=brigada_id, integrante_id=integrante_id)
    except ValueError as e:
        msg = str(e)
        status_code = (
            status.HTTP_409_CONFLICT if "mínimos" in msg.lower() else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail=msg)