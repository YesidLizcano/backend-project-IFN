from fastapi import APIRouter, HTTPException, status

from fastapi import Depends

from src.Modules.MaterialEquipo.Application.materialEquipo_crear import CrearMaterialEquipo
from src.Modules.MaterialEquipo.Domain.materialEquipo import MaterialEquipoCrear, MaterialEquipoSalida
from src.Modules.MaterialEquipo.Domain.materialEquipo_repository import MaterialEquipoRepository
from src.Modules.MaterialEquipo.Infrastructure.Persistence.DBMaterialEquipoRepository import get_material_equipo_repository
from src.Shared.Domain.departamento_repository import DepartamentoRepository
from src.Shared.Infrastructure.Persistence.DBDepartamentoRepository import get_departamento_repository



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
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository)
):
    try:
        creator = CrearMaterialEquipo(material_equipo_repo, departamento_repo)
        saved_material_equipo = creator.execute(material_equipo_data, departamento_id)
        return saved_material_equipo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
