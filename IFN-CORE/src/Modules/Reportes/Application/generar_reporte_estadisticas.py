from datetime import date
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.Reportes.Domain.reporte import ReporteEstadisticas

class GenerarReporteEstadisticas:
    def __init__(self, repository: ReporteRepository):
        self.repository = repository

    def execute(self) -> ReporteEstadisticas:
        datos = self.repository.generar_reporte_estadisticas()
        
        return ReporteEstadisticas(
            nombre="Reporte de Estadísticas Generales",
            fecha_generacion=date.today().isoformat(),
            datos=[], # No hay lista de datos detallados en este reporte resumen
            total_conglomerados=datos["total_conglomerados"],
            total_integrantes_activos_disponibles=datos["total_integrantes_activos_disponibles"],
            total_brigadas_activas=datos["total_brigadas_activas"]
        )
