from fastapi import APIRouter, Depends, status
from src.Modules.Reportes.Application.generar_reporte_inventario import GenerarReporteInventario
from src.Modules.Reportes.Domain.reporte import ReporteInventario
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.Reportes.Infrastructure.Persistence.DBReporteRepository import get_reporte_repository
from src.Shared.Auth.Domain.auth_service_interface import TokenPayload
from src.Shared.Auth.Infrastructure.dependencies import get_token_payload
from src.Shared.database import SessionDep

router = APIRouter(tags=["reportes"])

@router.get(
    "/reportes/inventario",
    response_model=ReporteInventario,
    status_code=status.HTTP_200_OK,
)
async def obtener_reporte_inventario(
    nombre_departamento: str,
    reporte_repo: ReporteRepository = Depends(get_reporte_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    generador = GenerarReporteInventario(reporte_repo)
    return generador.execute(nombre_departamento)
