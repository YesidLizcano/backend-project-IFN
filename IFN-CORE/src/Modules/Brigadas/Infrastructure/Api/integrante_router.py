from fastapi import APIRouter, status, HTTPException
from fastapi import Depends
from typing import List
from datetime import date

from src.Modules.Brigadas.Application.integrante_crear import CrearIntegrante
from src.Modules.Brigadas.Application.integrante_listar_por_region import IntegranteListarPorRegion
from src.Modules.Brigadas.Domain.integrante import IntegranteCrear, IntegranteSalida
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteRepository import get_integrante_repository
from src.Shared.Domain.municipio_repository import MunicipioRepository
from src.Shared.Infrastructure.Persistence.DBMunicipioRepository import get_municipio_repository
from src.Shared.Domain.departamento_repository import DepartamentoRepository
from src.Shared.Infrastructure.Persistence.DBDepartamentoRepository import get_departamento_repository


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


@router.get(
    "/integrantes/region/{departamento_id}",
    response_model=List[IntegranteSalida],
    status_code=status.HTTP_200_OK,
)
async def listar_integrantes_por_region(
    departamento_id: int,
    fechaInicio: date,
    fechaFinAprox: date,
    rol: str,
    integrante_repo: IntegranteRepository = Depends(get_integrante_repository),
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository),
):
    """
    Lista todos los integrantes activos que pertenecen a la misma región 
    que el departamento especificado, disponibles en el rango de fechas
    y que tienen el rol especificado.
    """
    try:
        # Validación simple: ambas fechas deben venir (FastAPI ya las marca como obligatorias)
        if not fechaInicio or not fechaFinAprox:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debe proporcionar fechaInicio y fechaFinAprox")

        # Usar el caso de uso de integrantes por región
        caso_uso = IntegranteListarPorRegion(integrante_repo, departamento_repo)
        integrantes = caso_uso.execute(departamento_id, fechaInicio, fechaFinAprox, rol)
        return integrantes
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error al listar integrantes por región: {str(e)}"
        )
