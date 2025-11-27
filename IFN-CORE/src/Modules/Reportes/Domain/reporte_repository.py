from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ReporteRepository(ABC):
    @abstractmethod
    def generar_reporte_inventario(self, nombre_departamento: str) -> List[Dict[str, Any]]:
        """Genera los datos para el reporte de inventario de un departamento."""
        pass

    @abstractmethod
    def generar_reporte_brigadas(self) -> List[Dict[str, Any]]:
        """Genera los datos para el reporte de todas las brigadas."""
        pass

    @abstractmethod
    def generar_reporte_conglomerados(self) -> List[Dict[str, Any]]:
        """Genera los datos para el reporte de todos los conglomerados."""
        pass

    @abstractmethod
    def generar_reporte_estadisticas(self) -> Dict[str, int]:
        """Genera las estadísticas generales del sistema."""
        pass

    @abstractmethod
    def generar_reporte_investigacion(self, conglomerado_id: int) -> Dict[str, Any]:
        """Genera un reporte detallado de una investigación por ID de conglomerado."""
        pass
