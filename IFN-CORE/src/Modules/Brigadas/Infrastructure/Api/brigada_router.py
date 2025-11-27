from fastapi import APIRouter, Depends, status, HTTPException

from src.Modules.Brigadas.Application.brigada_crear import CrearBrigada
from src.Modules.Brigadas.Application.brigada_listar import ListarBrigadas
from src.Modules.Brigadas.Application.brigada_eliminar import EliminarBrigada
from src.Modules.Brigadas.Domain.brigada import BrigadaCrear, BrigadaSalida
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Brigadas.Domain.integranteBrigada_repository import IntegranteBrigadaRepository
from src.Modules.Brigadas.Infrastructure.Persistence.DBBrigadaRepository import get_brigada_repository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteRepository import get_integrante_repository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteBrigadaRepository import get_integrante_brigada_repository
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Infrastructure.Persistence.DBConglomeradoRepository import get_conglomerado_repository
from src.Modules.MaterialEquipo.Domain.controlEquipo_repository import ControlEquipoRepository
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.DBControlEquipoRepository import get_control_equipo_repository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.DBMaterialEquipoRepository import get_material_equipo_repository
from src.Shared.Auth.Domain.auth_service_interface import TokenPayload
from src.Shared.Auth.Infrastructure.dependencies import get_token_payload
from src.Shared.database import SessionDep


router = APIRouter(tags=["brigadas"])


@router.post(
    "/brigadas/{conglomerado_id}",
    response_model=BrigadaSalida,
    status_code=status.HTTP_201_CREATED,
)
async def crear_brigada(
    conglomerado_id: int,
    brigada_data: BrigadaCrear,
    session: SessionDep,
    token_payload: TokenPayload = Depends(get_token_payload),
):
    brigada_repo: BrigadaRepository = get_brigada_repository(session=session)
    conglomerado_repo: ConglomeradoRepository = get_conglomerado_repository(session=session)
    integrante_repo: IntegranteRepository = get_integrante_repository(session=session)
    integrante_brigada_repo: IntegranteBrigadaRepository = get_integrante_brigada_repository(session=session)
    control_equipo_repo: ControlEquipoRepository = get_control_equipo_repository(session=session)
    material_equipo_repo: MaterialEquipoRepository = get_material_equipo_repository(session=session)
    try:
        creator = CrearBrigada(
            brigada_repository=brigada_repo,
            conglomerado_repository=conglomerado_repo,
            integrante_repository=integrante_repo,
            integrante_brigada_repository=integrante_brigada_repo,
            control_equipo_repository=control_equipo_repo,
            material_equipo_repository=material_equipo_repo,
            session=session,
        )
        saved_brigada = creator.execute(brigada_data, conglomerado_id)
        return saved_brigada
    except ValueError as e:
        msg = str(e)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if "no encontrado" in msg.lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=msg)


@router.delete(
    "/brigadas/{brigada_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def eliminar_brigada(
    brigada_id: int,
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Elimina una brigada existente por su identificador."""
    try:
        eliminador = EliminarBrigada(
            brigada_repository=brigada_repo,
            conglomerado_repository=conglomerado_repo,
        )
        eliminador.execute(brigada_id)
    except ValueError as e:
        msg = str(e)
        status_code = (
            status.HTTP_409_CONFLICT
            if "ya inició" in msg.lower()
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail=msg)


@router.get(
    "/brigadas",
    response_model=list[BrigadaSalida],
    status_code=status.HTTP_200_OK,
)
async def listar_brigadas(
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Lista todas las brigadas registradas."""
    listador = ListarBrigadas(brigada_repo)
    return listador.execute()