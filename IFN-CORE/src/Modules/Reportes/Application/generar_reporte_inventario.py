from datetime import datetime
from typing import List, Dict, Any
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.Reportes.Domain.reporte import ReporteInventario

class GenerarReporteInventario:
    def __init__(self, reporte_repository: ReporteRepository):
        self.reporte_repository = reporte_repository

    def execute(self, nombre_departamento: str) -> ReporteInventario:
        datos = self.reporte_repository.generar_reporte_inventario(nombre_departamento)
        
        return ReporteInventario(
            nombre="Reporte de Inventario",
            fecha_generacion=datetime.now().isoformat(),
            datos=datos,
            departamento=nombre_departamento,
            total_items=len(datos)
        )
