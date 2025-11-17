from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.Modules.Ubicacion.Application.departamento_crear import CrearDepartamento
from src.Modules.Ubicacion.Application.departamento_listar import ListarDepartamentos
from src.Modules.Ubicacion.Domain.departamento import Departamento, DepartamentoSalida
from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository
from src.Modules.Ubicacion.Infrastructure.Persistence.DBDepartamentoRepository import get_departamento_repository
from src.Shared.Auth.Domain.auth_service_interface import TokenPayload
from src.Shared.Auth.Infrastructure.dependencies import get_token_payload

router = APIRouter(tags = ['departamentos'])


@router.post(
    "/departamentos",
    response_model=DepartamentoSalida,
    status_code=status.HTTP_201_CREATED
)
async def crear_departamento(
    departamento_data: Departamento,
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    try:
        creador = CrearDepartamento(departamento_repo)
        departamento_guardado = creador.execute(departamento_data)
        return departamento_guardado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/departamentos", response_model=list[DepartamentoSalida])
async def listar_departamentos(
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    listador = ListarDepartamentos(departamento_repo)
    return listador.execute()