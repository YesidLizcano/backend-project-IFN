from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import EmailStr
from src.Modules.Reportes.Application.generar_reporte_inventario import GenerarReporteInventario
from src.Modules.Reportes.Application.generar_reporte_brigadas import GenerarReporteBrigadas
from src.Modules.Reportes.Application.generar_reporte_conglomerados import GenerarReporteConglomerados
from src.Modules.Reportes.Application.generar_reporte_estadisticas import GenerarReporteEstadisticas
from src.Modules.Reportes.Application.generar_reporte_investigacion import GenerarReporteInvestigacion
from src.Modules.Reportes.Domain.reporte import ReporteInventario, ReporteBrigadas, ReporteConglomerados, ReporteEstadisticas, ReporteInvestigacion
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.Reportes.Infrastructure.Persistence.DBReporteRepository import get_reporte_repository
from src.Shared.Services.pdf_service import PDFService
from src.Shared.Services.email_service import EmailService
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

@router.get(
    "/reportes/brigadas",
    response_model=ReporteBrigadas,
    status_code=status.HTTP_200_OK,
)
async def obtener_reporte_brigadas(
    reporte_repo: ReporteRepository = Depends(get_reporte_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    generador = GenerarReporteBrigadas(reporte_repo)
    return generador.execute()

@router.get(
    "/reportes/conglomerados",
    response_model=ReporteConglomerados,
    status_code=status.HTTP_200_OK,
)
async def obtener_reporte_conglomerados(
    reporte_repo: ReporteRepository = Depends(get_reporte_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    generador = GenerarReporteConglomerados(reporte_repo)
    return generador.execute()

@router.get(
    "/reportes/estadisticas",
    response_model=ReporteEstadisticas,
    status_code=status.HTTP_200_OK,
)
async def obtener_reporte_estadisticas(
    reporte_repo: ReporteRepository = Depends(get_reporte_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    generador = GenerarReporteEstadisticas(reporte_repo)
    return generador.execute()

@router.get(
    "/reportes/investigacion/{conglomerado_id}",
    response_model=ReporteInvestigacion,
    status_code=status.HTTP_200_OK,
)
async def obtener_reporte_investigacion(
    conglomerado_id: int,
    email_destino: EmailStr,
    reporte_repo: ReporteRepository = Depends(get_reporte_repository),
    token_payload: TokenPayload = Depends(get_token_payload),
):
    try:
        generador = GenerarReporteInvestigacion(reporte_repo)
        reporte = generador.execute(conglomerado_id)
        
        # Generar PDF
        pdf_service = PDFService()
        pdf_bytes = pdf_service.generar_reporte_investigacion(reporte)
        
        # Enviar Email
        email_service = EmailService()
        await email_service.send_email_with_pdf(
            email_to=email_destino,
            subject=f"Reporte de Investigación - Conglomerado {conglomerado_id}",
            body=f"Adjunto encontrará el reporte detallado del conglomerado {conglomerado_id}.",
            pdf_content=pdf_bytes,
            pdf_filename=f"reporte_conglomerado_{conglomerado_id}.pdf"
        )
        
        return reporte
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
