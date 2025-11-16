from fastapi import APIRouter, Depends, HTTPException, status

from src.Shared.Application.municipio_crear import CrearMunicipio
from src.Shared.Domain.departamento_repository import DepartamentoRepository
from src.Shared.Domain.municipio import MunicipioCrear, MunicipioSalida
from src.Shared.Domain.municipio_repository import MunicipioRepository
from src.Shared.Infrastructure.Persistence.DBDepartamentoRepository import get_departamento_repository
from src.Shared.Infrastructure.Persistence.DBMunicipioRepository import get_municipio_repository

router = APIRouter(tags = ['municipios'])


@router.post(
    "/municipios/{departamento_id}",
    response_model=MunicipioSalida,
    status_code=status.HTTP_201_CREATED
)
async def crear_municipio(
    departamento_id: int,
    municipio_data: MunicipioCrear,
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository),
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository)
):
    """
    Crea un nuevo municipio asociado al departamento especificado.
    
    Args:
        departamento_id: ID del departamento al que pertenece el municipio
        municipio_data: Datos del municipio a crear (nombre)
    """
    try:
        creator = CrearMunicipio(municipio_repo, departamento_repo)
        saved_municipio = creator.execute(municipio_data, departamento_id)
        return saved_municipio
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/municipios", response_model=list[MunicipioSalida])
async def listar_municipios(municipio_repo: MunicipioRepository = Depends(get_municipio_repository)):
    return municipio_repo.listar_municipios()
