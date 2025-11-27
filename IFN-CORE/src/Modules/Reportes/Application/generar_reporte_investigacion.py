from datetime import date
from src.Modules.Reportes.Domain.reporte_repository import ReporteRepository
from src.Modules.Reportes.Domain.reporte import ReporteInvestigacion

class GenerarReporteInvestigacion:
    def __init__(self, repository: ReporteRepository):
        self.repository = repository

    def execute(self, conglomerado_id: int) -> ReporteInvestigacion:
        datos = self.repository.generar_reporte_investigacion(conglomerado_id)
        
        if not datos:
            raise ValueError(f"No se encontró información para el conglomerado {conglomerado_id}")

        return ReporteInvestigacion(
            nombre=f"Reporte de Investigación - Conglomerado {conglomerado_id}",
            fecha_generacion=date.today().isoformat(),
            datos=[],
            conglomerado=datos["conglomerado"],
            subparcelas=datos["subparcelas"],
            brigada=datos["brigada"],
            integrantes=datos["integrantes"],
            materiales_equipos=datos["materiales_equipos"]
        )
