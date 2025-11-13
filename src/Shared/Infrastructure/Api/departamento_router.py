from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.Shared.Application.departamento_crear import CrearDepartamento
from src.Shared.Application.departamento_listar import ListarDepartamentos
from src.Shared.Domain.departamento import Departamento, DepartamentoSalida
from src.Shared.Domain.departamento_repository import DepartamentoRepository
from src.Shared.Infrastructure.Persistence.DBDepartamentoRepository import get_departamento_repository

router = APIRouter(tags = ['departamentos'])


@router.post(
    "/departamentos",
    response_model=DepartamentoSalida,
    status_code=status.HTTP_201_CREATED
)
async def crear_departamento(
    departamento_data: Departamento,
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository)
):
    try:
        creador = CrearDepartamento(departamento_repo)
        departamento_guardado = creador.execute(departamento_data)
        return departamento_guardado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/departamentos", response_model=list[DepartamentoSalida])
async def listar_departamentos(
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository)
):
    listador = ListarDepartamentos(departamento_repo)
    return listador.execute()