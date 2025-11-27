from datetime import date
from fastapi import APIRouter, HTTPException, status

from fastapi import Depends

from src.Modules.MaterialEquipo.Application.materialEquipo_crear import CrearMaterialEquipo
from src.Modules.MaterialEquipo.Application.materialEquipo_actualizar import ActualizarMaterialEquipo
from src.Modules.MaterialEquipo.Application.materialEquipo_eliminar import EliminarMaterialEquipo
from src.Modules.MaterialEquipo.Application.materialEquipo_listar import (
    ListarMaterialesEquipo,
)
from src.Modules.MaterialEquipo.Application.controlEquipo_asignacion_defecto import AsignarMaterialesPorDefectoABrigada
from src.Modules.MaterialEquipo.Domain.materialEquipo import MaterialEquipoActualizar, MaterialEquipoCrear, MaterialEquipoSalida
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.DBMaterialEquipoRepository import get_material_equipo_repository
from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository
from src.Modules.Ubicacion.Infrastructure.Persistence.DBDepartamentoRepository import get_departamento_repository
from src.Modules.MaterialEquipo.Domain.controlEquipo_repository import ControlEquipoRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.DBControlEquipoRepository import get_control_equipo_repository
from src.Shared.Auth.Domain.auth_service_interface import TokenPayload
from src.Shared.Auth.Infrastructure.dependencies import get_token_payload



router = APIRouter(tags=["materiales_equipos"])


@router.post(
    "/materiales_equipos/{departamento_id}",
    response_model=MaterialEquipoSalida,
    status_code=status.HTTP_201_CREATED,
)
async def crear_material_equipo(
    departamento_id: int,
    material_equipo_data: MaterialEquipoCrear,
    material_equipo_repo: MaterialEquipoRepository = Depends(get_material_equipo_repository),
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    try:
        creator = CrearMaterialEquipo(material_equipo_repo, departamento_repo)
        saved_material_equipo = creator.execute(material_equipo_data, departamento_id)
        return saved_material_equipo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch(
    "/materiales_equipos/{material_equipo_id}",
    response_model=MaterialEquipoSalida,
    status_code=status.HTTP_200_OK,
)
async def actualizar_material_equipo(
    material_equipo_id: int,
    material_equipo_data: MaterialEquipoActualizar,
    material_equipo_repo: MaterialEquipoRepository = Depends(get_material_equipo_repository),
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository),
    control_equipo_repo: ControlEquipoRepository = Depends(get_control_equipo_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Actualiza parcialmente un MaterialEquipo: nombre, cantidad y/o departamento_id."""
    try:
        updater = ActualizarMaterialEquipo(
            material_equipo_repository=material_equipo_repo,
            departamento_repository=departamento_repo,
            control_equipo_repository=control_equipo_repo,
        )
        actualizado = updater.execute(material_equipo_id, material_equipo_data)
        return actualizado
    except ValueError as e:
        msg = str(e)
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if "al menos un campo" in msg.lower() or "no puede ser" in msg.lower()
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail=msg)


@router.delete(
    "/materiales_equipos/{material_equipo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def eliminar_material_equipo(
    material_equipo_id: int,
    material_equipo_repo: MaterialEquipoRepository = Depends(get_material_equipo_repository),
    control_equipo_repo: ControlEquipoRepository = Depends(get_control_equipo_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Elimina un Material/Equipo si no tiene asignaciones activas desde hoy."""
    try:
        eliminador = EliminarMaterialEquipo(
            material_equipo_repository=material_equipo_repo,
            control_equipo_repository=control_equipo_repo,
        )
        eliminador.execute(material_equipo_id)
        return None
    except ValueError as e:
        msg = str(e)
        if "no se puede eliminar" in msg.lower() or "asignadas" in msg.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


@router.get(
    "/materiales_equipos",
    response_model=list[MaterialEquipoSalida],
    status_code=status.HTTP_200_OK,
)
async def listar_materiales_equipo(
    nombre_departamento: str,
    material_equipo_repo: MaterialEquipoRepository = Depends(get_material_equipo_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Lista materiales/equipos filtrando por `nombre_departamento` (query param)."""
    lister = ListarMaterialesEquipo(material_equipo_repo)
    return lister.execute(nombre_departamento)


@router.get(
    "/control-equipos/asignacion-defecto",
    status_code=status.HTTP_200_OK,
)
async def listar_asignacion_por_defecto(
    nombre_departamento: str,
    fecha_inicio: date,
    fecha_fin_aprox: date,
    control_equipo_repo: ControlEquipoRepository = Depends(get_control_equipo_repository),
    material_equipo_repo: MaterialEquipoRepository = Depends(get_material_equipo_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Lista la propuesta de asignación por defecto de materiales/equipos.

    Simula qué se asignaría basado en fechas y disponibilidad en el departamento indicado (por nombre).
    """
    try:
        caso_uso = AsignarMaterialesPorDefectoABrigada(
            control_equipo_repo,
            material_equipo_repo,
        )
        resumen = caso_uso.execute(nombre_departamento, fecha_inicio, fecha_fin_aprox)
        return resumen
    except ValueError as e:
        msg = str(e)
        if "fechas" in msg.lower() or "no se puede asignar por defecto" in msg.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
