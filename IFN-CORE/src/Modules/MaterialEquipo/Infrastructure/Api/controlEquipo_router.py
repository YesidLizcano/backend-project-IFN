from fastapi import APIRouter, Depends, status, HTTPException

from src.Modules.MaterialEquipo.Application.controlEquipo_crear import CrearControlEquipo
from src.Modules.MaterialEquipo.Application.controlEquipo_asignacion_defecto import AsignarMaterialesPorDefectoABrigada
from src.Modules.MaterialEquipo.Domain.controlEquipo import ControlEquipo, ControlEquipoCrear
from src.Modules.MaterialEquipo.Domain.controlEquipo_repository import ControlEquipoRepository
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.DBControlEquipoRepository import get_control_equipo_repository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.DBMaterialEquipoRepository import get_material_equipo_repository
from src.Modules.Brigadas.Infrastructure.Persistence.DBBrigadaRepository import get_brigada_repository
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Infrastructure.Persistence.DBConglomeradoRepository import get_conglomerado_repository
from src.Shared.Domain.municipio_repository import MunicipioRepository
from src.Shared.Infrastructure.Persistence.DBMunicipioRepository import get_municipio_repository


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
):
    control_equipo = control_equipo_repo.buscar_por_id(control_equipo_id)
    if not control_equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Control de equipo con ID {control_equipo_id} no encontrado"
        )
    return control_equipo


@router.post(
    "/brigadas/{brigada_id}/control-equipos/asignacion-defecto",
    status_code=status.HTTP_201_CREATED,
)
async def asignar_por_defecto(
    brigada_id: int,
    control_equipo_repo: ControlEquipoRepository = Depends(get_control_equipo_repository),
    material_equipo_repo: MaterialEquipoRepository = Depends(get_material_equipo_repository),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository),
):
    """Asigna cantidades por defecto de materiales/equipos a la brigada.

    Usa fechas del conglomerado (inicio y fin aprox) y el departamento del
    municipio para localizar los materiales por nombre.
    """
    try:
        caso_uso = AsignarMaterialesPorDefectoABrigada(
            control_equipo_repo,
            material_equipo_repo,
            brigada_repo,
            conglomerado_repo,
            municipio_repo,
        )
        resumen = caso_uso.execute(brigada_id)
        return resumen
    except ValueError as e:
        msg = str(e)
        if "fechas" in msg.lower() or "no se puede asignar por defecto" in msg.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
