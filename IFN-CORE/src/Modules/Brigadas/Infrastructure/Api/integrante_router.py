from fastapi import APIRouter, status, HTTPException
from fastapi import Depends
from typing import List
from datetime import date

from src.Modules.Brigadas.Application.integrante_crear import CrearIntegrante
from src.Modules.Brigadas.Application.integrante_listar_por_region import IntegranteListarPorRegion
from src.Modules.Brigadas.Application.integrante_listar_por_brigada import IntegranteListarPorBrigada
from src.Modules.Brigadas.Application.integrante_eliminar import EliminarIntegrante
from src.Modules.Brigadas.Application.integrante_actualizar import ActualizarIntegrante
from src.Modules.Brigadas.Domain.integrante import IntegranteActualizar
from src.Modules.Brigadas.Domain.integrante import IntegranteCrear, IntegranteSalida
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteRepository import get_integrante_repository
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository
from src.Modules.Ubicacion.Infrastructure.Persistence.DBMunicipioRepository import get_municipio_repository
from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository
from src.Modules.Ubicacion.Infrastructure.Persistence.DBDepartamentoRepository import get_departamento_repository
from src.Shared.Auth.Domain.auth_service_interface import TokenPayload
from src.Shared.Auth.Infrastructure.dependencies import get_token_payload


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
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    try:
        creator = CrearIntegrante(integrante_repo, municipio_repo)
        saved_integrante = creator.execute(integrante_data, municipio_id)
        return saved_integrante
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/integrantes/region/{departamento_nombre}",
    response_model=List[IntegranteSalida],
    status_code=status.HTTP_200_OK,
)
async def listar_integrantes_por_region(
    departamento_nombre: str,
    fechaInicio: date,
    fechaFinAprox: date,
    integrante_repo: IntegranteRepository = Depends(get_integrante_repository),
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """
    Lista todos los integrantes activos que pertenecen a la misma región
    que el departamento especificado y que están disponibles en el rango de fechas.
    """
    try:
        # Validación simple: ambas fechas deben venir (FastAPI ya las marca como obligatorias)
        if not fechaInicio or not fechaFinAprox:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debe proporcionar fechaInicio y fechaFinAprox")

        # Buscar departamento por nombre (insensible a mayúsculas)
        departamento = departamento_repo.buscar_por_nombre(departamento_nombre)
        if not departamento:
            raise ValueError(f"Departamento '{departamento_nombre}' no encontrado")

        # Usar el caso de uso de integrantes por región
        caso_uso = IntegranteListarPorRegion(integrante_repo, departamento_repo)
        integrantes = caso_uso.execute(departamento.id, fechaInicio, fechaFinAprox)
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


@router.get(
    "/integrantes/brigada/{brigada_id}",
    response_model=List[IntegranteSalida],
    status_code=status.HTTP_200_OK,
)
async def listar_integrantes_por_brigada(
    brigada_id: int,
    integrante_repo: IntegranteRepository = Depends(get_integrante_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """
    Lista todos los integrantes asociados a una brigada específica.
    """
    try:
        caso_uso = IntegranteListarPorBrigada(integrante_repo)
        return caso_uso.execute(brigada_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar integrantes por brigada: {str(e)}"
        )


@router.patch(
    "/integrantes/{integrante_id}",
    response_model=IntegranteSalida,
    status_code=status.HTTP_200_OK,
)
async def actualizar_integrante(
    integrante_id: int,
    cambios: IntegranteActualizar,
    integrante_repo: IntegranteRepository = Depends(get_integrante_repository),
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Actualiza parcialmente un integrante.

    Si el nuevo estado es distinto de ACTIVO_DISPONIBLE, valida que no tenga
    asignaciones futuras.
    """
    try:
        caso_uso = ActualizarIntegrante(integrante_repo, municipio_repo)
        actualizado = caso_uso.execute(integrante_id, cambios)
        return actualizado
    except ValueError as e:
        msg = str(e)
        if "asignaciones futuras" in msg.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
        if "al menos un campo" in msg.lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
        if "municipio no encontrado" in msg.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


@router.delete(
    "/integrantes/{integrante_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def eliminar_integrante(
    integrante_id: int,
    integrante_repo: IntegranteRepository = Depends(get_integrante_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Elimina un integrante si no tiene asignaciones con fecha de inicio futura."""
    try:
        caso_uso = EliminarIntegrante(integrante_repo)
        caso_uso.execute(integrante_id)
        return None
    except ValueError as e:
        msg = str(e)
        if "no se puede eliminar" in msg.lower() or "no ha iniciado" in msg.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
