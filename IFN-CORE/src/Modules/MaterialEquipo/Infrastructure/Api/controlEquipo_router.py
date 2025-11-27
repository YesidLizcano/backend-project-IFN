from datetime import date
from fastapi import APIRouter, Depends, status, HTTPException, Query

from src.Modules.MaterialEquipo.Application.controlEquipo_crear import CrearControlEquipo
from src.Modules.MaterialEquipo.Domain.controlEquipo import ControlEquipo, ControlEquipoCrear
from src.Modules.MaterialEquipo.Domain.controlEquipo_repository import ControlEquipoRepository
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.DBControlEquipoRepository import get_control_equipo_repository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.DBMaterialEquipoRepository import get_material_equipo_repository
from src.Modules.Brigadas.Infrastructure.Persistence.DBBrigadaRepository import get_brigada_repository
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Infrastructure.Persistence.DBConglomeradoRepository import get_conglomerado_repository
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository
from src.Modules.Ubicacion.Infrastructure.Persistence.DBMunicipioRepository import get_municipio_repository
from src.Shared.Auth.Domain.auth_service_interface import TokenPayload
from src.Shared.Auth.Infrastructure.dependencies import get_token_payload


router = APIRouter(tags=["control_equipo"])


@router.post(
    "/brigadas/{brigada_id}/material-equipos/{material_equipo_id}/control-equipos",
    response_model=ControlEquipo,
    status_code=status.HTTP_201_CREATED,
)
async def crear_control_equipo(
    brigada_id: int,
    material_equipo_id: int,
    control_equipo_data: ControlEquipoCrear,
    control_equipo_repo: ControlEquipoRepository = Depends(get_control_equipo_repository),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    material_equipo_repo: MaterialEquipoRepository = Depends(get_material_equipo_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    try:
        creator = CrearControlEquipo(control_equipo_repo, brigada_repo, material_equipo_repo)
        saved_control_equipo = creator.execute(control_equipo_data, brigada_id, material_equipo_id)
        return saved_control_equipo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))




@router.get(
    "/control-equipos/{control_equipo_id}",
    response_model=ControlEquipo,
    status_code=status.HTTP_200_OK,
)
async def obtener_control_equipo(
    control_equipo_id: int,
    control_equipo_repo: ControlEquipoRepository = Depends(get_control_equipo_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    control_equipo = control_equipo_repo.buscar_por_id(control_equipo_id)
    if not control_equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Control de equipo con ID {control_equipo_id} no encontrado"
        )
    return control_equipo
