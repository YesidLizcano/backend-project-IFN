from fastapi import APIRouter, HTTPException, status

from fastapi import Depends
import json
import os
import httpx
from fastapi import Body
from typing import List
from pydantic import BaseModel
from datetime import date

from src.Modules.Conglomerados.Domain.conglomerado import (
    Conglomerado, 
    ConglomeradoCrear, 
    ConglomeradoActualizarFechas,
    ConglomeradoFinalizar,
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
from src.Modules.Ubicacion.Application.departamento_listar_por_region import DepartamentoListarPorRegion
from src.Modules.Ubicacion.Infrastructure.Persistence.DBDepartamentoRepository import get_departamento_repository
from src.Modules.Conglomerados.Application.conglomerado_actualizar_fechas import ActualizarFechasConglomerado
from src.Modules.Conglomerados.Application.conglomerado_finalizar import FinalizarConglomerado
from src.Modules.Conglomerados.Application.conglomerado_eliminar import EliminarConglomerado
from src.Modules.Ubicacion.Domain.municipio_repository import MunicipioRepository
from src.Modules.Ubicacion.Domain.municipio import MunicipioCrear, Municipio
from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository
from src.Modules.Ubicacion.Infrastructure.Persistence.DBMunicipioRepository import (
    get_municipio_repository,
)
from src.Modules.Ubicacion.Infrastructure.Persistence.DBDepartamentoRepository import (
    get_departamento_repository,
)
from src.Shared.Auth.Domain.auth_service_interface import TokenPayload
from src.Shared.Auth.Infrastructure.dependencies import get_token_payload



router = APIRouter(tags=["conglomerados"])
# ...existing code...



@router.post("/conglomerados/verificar-en-colombia", response_model=List[dict])
async def verificar_puntos_en_colombia(
    body: VerificarPuntosRequest,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    departamento_repo = Depends(get_departamento_repository),
    token_payload: TokenPayload = Depends(get_token_payload)
):
    """
    Verifica si cada punto (lon, lat) está dentro de Colombia y enriquece con municipio/departamento/region usando OpenCage y lógica local.
    """
    creator = CrearConglomerado(conglomerado_repo, None)
    region_helper = DepartamentoListarPorRegion(departamento_repo)
    api_key = os.environ.get("OPENCAGE_API_KEY")
    if not api_key:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se configuró OPENCAGE_API_KEY")

    resultados = []
    async with httpx.AsyncClient() as client:
        for p in body.puntos:
            if not creator.conglomerado_en_colombia(p.lon, p.lat):
                continue
            municipio = "No Encontrado"
            departamento = "No Encontrado"
            region = "No Encontrado"
            try:
                url = f"https://api.opencagedata.com/geocode/v1/json?q={p.lat},{p.lon}&key={api_key}&language=es"
                resp = await client.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("results"):
                        comp = data["results"][0].get("components", {})
                        departamento = comp.get("state", "No Encontrado")
                        municipio = comp.get("city") or comp.get("town") or comp.get("county") or "No Encontrado"
                        region = region_helper.obtener_nombre_region(departamento) if departamento != "No Encontrado" else "No Encontrado"
                elif resp.status_code == 402:
                    # Límite de uso alcanzado
                    raise HTTPException(status_code=429, detail="Límite de uso de OpenCage alcanzado. Espera o usa otra clave.")
                elif resp.status_code == 403:
                    # Clave inválida
                    raise HTTPException(status_code=502, detail="API Key de OpenCage inválida o bloqueada.")
                else:
                    raise HTTPException(status_code=502, detail=f"Error en OpenCage: {resp.status_code}")
            except httpx.TimeoutException:
                raise HTTPException(status_code=504, detail="Timeout al consultar OpenCage. Intenta de nuevo más tarde.")
            except httpx.HTTPError as e:
                raise HTTPException(status_code=502, detail=f"Error HTTP al consultar OpenCage: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error inesperado en la verificación: {str(e)}")
            resultados.append({
                "lat": p.lat,
                "lon": p.lon,
                "departamento": departamento,
                "municipio": municipio,
                "region": region
            })
    return resultados



@router.get(
    "/conglomerados",
    response_model=List[dict],
)
async def listar_conglomerados(
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository),
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """Lista conglomerados incluyendo el nombre del municipio y departamento asociados."""
    resultados = []
    region_helper = DepartamentoListarPorRegion(departamento_repo)
    try:
        conglomerados = conglomerado_repo.listar_conglomerados()

        for c in conglomerados:
            # c es un DTO ConglomeradoSalida
            municipio_nombre = "No Encontrado"
            departamento_nombre = "No Encontrado"
            region_nombre = "No Encontrado"
            estado = "Sin Asignar"
            try:
                municipio = municipio_repo.buscar_por_id(c.municipio_id)
                if municipio:
                    municipio_nombre = municipio.nombre
                    departamento = departamento_repo.buscar_por_id(municipio.departamento_id)
                    if departamento:
                        departamento_nombre = departamento.nombre
                        # Obtener región a partir del nombre de departamento
                        try:
                            region_nombre = region_helper.obtener_nombre_region(departamento_nombre)
                        except Exception:
                            region_nombre = "No Encontrado"
                # Determinar estado según existencia de brigada y fechas
                brigada = brigada_repo.buscar_por_conglomerado_id(c.id)
                if not brigada:
                    estado = "Sin Asignar"
                else:
                    # Si existe brigada, revisar fechas del conglomerado
                    hoy = date.today()
                    fecha_fin = getattr(c, "fechaFin", None)
                    fecha_fin_aprox = getattr(c, "fechaFinAprox", None)
                    fecha_inicio = getattr(c, "fechaInicio", None)
                    try:
                        # Si ya existe fechaFin registrada y es pasada -> Finalizado
                        if fecha_fin and fecha_fin <= hoy:
                            estado = "Finalizado"
                        # Si la fechaFinAprox pasó pero no hay fechaFin real -> Pendiente de Cierre
                        elif fecha_fin_aprox and fecha_fin_aprox < hoy and not fecha_fin:
                            estado = "Pendiente de Cierre"
                        elif fecha_inicio and fecha_inicio <= hoy:
                            estado = "En Exploracion"                            
                        elif fecha_inicio and fecha_inicio > hoy:
                            estado = "Asignado"
                        else:
                            # Si no hay fechas claras, considerar asignado
                            estado = "Asignado"
                    except Exception:
                        # En caso de formatos inesperados, mantener asignado
                        estado = "Asignado"
            except Exception:
                # Silencioso: mantén valores por defecto si hay error en consulta
                pass

            # Agregar datos del conglomerado y nombres asociados
            data = c.model_dump() if hasattr(c, "model_dump") else c.model_dump()
            data.update({
                "municipio_nombre": municipio_nombre,
                "departamento_nombre": departamento_nombre,
                "region": region_nombre,
                "estado": estado,
            })
            resultados.append(data)

        return resultados
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/conglomerados/municipio/{municipio_nombre}/departamento/{departamento_nombre}",
    response_model=ConglomeradoSalida,
    status_code=status.HTTP_201_CREATED,
)
async def crear_conglomerado(
    municipio_nombre: str,
    departamento_nombre: str,
    conglomerado_data: ConglomeradoCrear,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    municipio_repo: MunicipioRepository = Depends(get_municipio_repository),
    departamento_repo: DepartamentoRepository = Depends(get_departamento_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    try:
        departamento = departamento_repo.buscar_por_nombre(departamento_nombre)
        if not departamento:
            raise ValueError("Departamento no encontrado")
        municipio = municipio_repo.buscar_por_nombre(municipio_nombre)
        if not municipio:
            # Crear municipio si no existe
            municipio_entidad = Municipio(nombre=municipio_nombre, departamento_id=departamento.id)
            municipio = municipio_repo.guardar(municipio_entidad)
        creator = CrearConglomerado(conglomerado_repo, municipio_repo)
        saved_conglomerado = creator.execute(conglomerado_data, municipio.id)
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


@router.patch(
    "/conglomerados/{conglomerado_id}/finalizar",
    response_model=ConglomeradoSalida,
    status_code=status.HTTP_200_OK,
)
async def finalizar_conglomerado(
    conglomerado_id: int,
    datos: ConglomeradoFinalizar,
    conglomerado_repo: ConglomeradoRepository = Depends(get_conglomerado_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    """
    Finaliza un conglomerado estableciendo su fechaFin real.
    Esto libera automáticamente a los integrantes asignados para fechas posteriores.
    """
    try:
        finalizador = FinalizarConglomerado(conglomerado_repo)
        return finalizador.execute(conglomerado_id, datos)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


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
        lower_msg = msg.lower()
        status_code = (
            status.HTTP_409_CONFLICT
            if any(trigger in lower_msg for trigger in ("brigada asociada", "fecha de inicio"))
            else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail=msg)


