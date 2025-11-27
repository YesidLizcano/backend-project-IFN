from datetime import datetime
from typing import List, Dict, Any
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.Reportes.Domain.reporte import ReporteConglomerados

class GenerarReporteConglomerados:
    def __init__(self, reporte_repository: ReporteRepository):
        self.reporte_repository = reporte_repository

    def execute(self) -> ReporteConglomerados:
        datos = self.reporte_repository.generar_reporte_conglomerados()
        
        return ReporteConglomerados(
            nombre="Reporte de Conglomerados",
            fecha_generacion=datetime.now().isoformat(),
            datos=datos,
            total_conglomerados=len(datos)
        )
