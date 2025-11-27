from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from src.Modules.Reportes.Domain.reporte import ReporteInvestigacion

class PDFService:
    def generar_reporte_investigacion(self, reporte: ReporteInvestigacion) -> bytes:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        y = height - 50
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, reporte.nombre)
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Fecha de Generación: {reporte.fecha_generacion}")
        y -= 40
        
        # Conglomerado
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Información del Conglomerado")
        y -= 20
        c.setFont("Helvetica", 10)
        cong = reporte.conglomerado
        c.drawString(60, y, f"Municipio: {cong.municipio}")
        y -= 15
        c.drawString(60, y, f"Coordenadas: {cong.latitud}, {cong.longitud}")
        y -= 15
        c.drawString(60, y, f"Fechas: {cong.fecha_inicio} - {cong.fecha_fin_aprox}")
        if cong.fecha_fin:
             y -= 15
             c.drawString(60, y, f"Fecha Fin Real: {cong.fecha_fin}")
        y -= 30
        
        # Subparcelas
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Subparcelas")
        y -= 20
        c.setFont("Helvetica", 10)
        for sub in reporte.subparcelas:
            # sub tiene campos 'latitud' y 'longitud'
            c.drawString(60, y, f"- Coordenadas: {sub.latitud}, {sub.longitud}")
            y -= 15
        y -= 15

        # Brigada
        if reporte.brigada:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Brigada Asignada")
            y -= 20
            c.setFont("Helvetica", 10)
            c.drawString(60, y, f"Estado: {reporte.brigada.estado}")
            y -= 15
            c.drawString(60, y, f"Fecha Creación: {reporte.brigada.fecha_creacion}")
            y -= 30
            
            # Integrantes
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Integrantes")
            y -= 20
            c.setFont("Helvetica", 10)
            for i in reporte.integrantes:
                c.drawString(60, y, f"- {i.nombre} ({i.rol}) - {i.email}")
                y -= 15
            y -= 15
            
            # Materiales
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Materiales y Equipos")
            y -= 20
            c.setFont("Helvetica", 10)
            for m in reporte.materiales_equipos:
                c.drawString(60, y, f"- {m.nombre}: {m.cantidad_asignada}")
                y -= 15
        else:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Sin Brigada Asignada")
            
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
