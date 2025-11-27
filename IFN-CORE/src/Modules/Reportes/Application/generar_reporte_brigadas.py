from datetime import datetime
from typing import List, Dict, Any
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.Reportes.Domain.reporte import ReporteBrigadas

class GenerarReporteBrigadas:
    def __init__(self, reporte_repository: ReporteRepository):
        self.reporte_repository = reporte_repository

    def execute(self) -> ReporteBrigadas:
        datos = self.reporte_repository.generar_reporte_brigadas()
        
        return ReporteBrigadas(
            nombre="Reporte de Brigadas",
            fecha_generacion=datetime.now().isoformat(),
            datos=datos,
            total_brigadas=len(datos)
        )
