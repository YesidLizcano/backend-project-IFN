from fastapi import APIRouter, HTTPException, status

from fastapi import Depends
import json

from src.Modules.Conglomerados.Domain.conglomerado import (
    Conglomerado, 
    ConglomeradoCrear, 
    ConglomeradoActualizarFechas,
    ConglomeradoSalida,
    PuntoCoords,
    VerificarPuntosRequest,
    VerificarPuntosResponse
)
from src.Modules.Conglomerados.Domain.conglomerado_repository import ConglomeradoRepository
from src.Modules.Conglomerados.Domain.subparcela_repository import SubparcelaRepository
from src.Modules.Conglomerados.Infrastructure.Persistence.DBConglomeradoRepository import get_conglomerado_repository
from src.Modules.Conglomerados.Infrastructure.Persistence.DBSubparcelaRepository import get_subparcela_repository
from src.Modules.Brigadas.Domain.brigada_repository import BrigadaRepository
from src.Modules.Brigadas.Infrastructure.Persistence.DBBrigadaRepository import get_brigada_repository
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Brigadas.Infrastructure.Persistence.DBIntegranteRepository import get_integrante_repository
from src.Modules.Conglomerados.Application.conglomerado_crear import CrearConglomerado
from fastapi import Body
from typing import List
from pydantic import BaseModel
from src.Modules.Conglomerados.Application.conglomerado_actualizar_fechas import ActualizarFechasConglomerado
from src.Modules.Conglomerados.Application.conglomerado_eliminar import EliminarConglomerado
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository
from src.Modules.Ubicacion.Infrastructure.Persistence.DBMunicipioRepository import (
    get_municipio_repository,
)
from src.Shared.Auth.Domain.auth_service_interface import TokenPayload
from src.Shared.Auth.Infrastructure.dependencies import get_token_payload



router = APIRouter(tags=["conglomerados"])
# ...existing code...

@router.post("/conglomerados/verificar-en-colombia", response_model=VerificarPuntosResponse)
async def verificar_puntos_en_colombia(
    body: VerificarPuntosRequest,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
):
    """
    Verifica si cada punto (lon, lat) está dentro de Colombia según colombia.geo.json.
    """
    # Usar la lógica de conglomerado_en_colombia de CrearConglomerado
    creator = CrearConglomerado(conglomerado_repo, None)
    resultados = [creator.conglomerado_en_colombia(p.lon, p.lat) for p in body.puntos]
    return VerificarPuntosResponse(resultados=resultados)


@router.post(
    "/conglomerados/{municipio_id}",
    response_model=ConglomeradoSalida,
    status_code=status.HTTP_201_CREATED,
)
async def crear_conglomerado(
    municipio_id: int,
    conglomerado_data: ConglomeradoCrear,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    try:
        creator = CrearConglomerado(conglomerado_repo, municipio_repo)
        saved_conglomerado = creator.execute(conglomerado_data, municipio_id)
        return saved_conglomerado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch(
    "/conglomerados/{conglomerado_id}/fechas",
    response_model=ConglomeradoSalida,
    status_code=status.HTTP_200_OK,
)
async def actualizar_fechas_conglomerado(
    conglomerado_id: int,
    fechas_data: ConglomeradoActualizarFechas,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    integrante_repo: IntegranteRepository = Depends(get_integrante_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """
    Actualiza las fechas (fechaInicio y fechaFinAprox) de un conglomerado existente.
    
    Args:
        conglomerado_id: ID del conglomerado a actualizar
        fechas_data: Nuevas fechas a asignar
    """
    try:
        actualizador = ActualizarFechasConglomerado(
            conglomerado_repository=conglomerado_repo,
            brigada_repository=brigada_repo,
            integrante_repository=integrante_repo,
        )
        conglomerado_actualizado = actualizador.execute(conglomerado_id, fechas_data)
        return conglomerado_actualizado
    except ValueError as e:
        msg = str(e)
        # Detectar payload de conflicto y responder 409 con detalle estructurado
        if msg.startswith("CONFLICTO_SOLAPAMIENTO:"):
            try:
                detalle = json.loads(msg.split(":", 1)[1])
            except Exception:
                detalle = {"tipo": "CONFLICTO_SOLAPAMIENTO", "mensaje": msg}
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detalle,
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error al actualizar fechas: {str(e)}"
        )


@router.delete(
    "/conglomerados/{conglomerado_id}",
    status_code=status.HTTP_200_OK,
)
async def eliminar_conglomerado(
    conglomerado_id: int,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    subparcela_repo: SubparcelaRepository = Depends(get_subparcela_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Elimina un conglomerado"""
    try:
        eliminador = EliminarConglomerado(
            conglomerado_repository=conglomerado_repo,
            brigada_repository=brigada_repo,
            subparcela_repository=subparcela_repo,
        )
        return eliminador.execute(conglomerado_id)
    except ValueError as e:
        msg = str(e)
        status_code = (
            status.HTTP_409_CONFLICT
            if "brigada asociada" in msg.lower()
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail=msg)


