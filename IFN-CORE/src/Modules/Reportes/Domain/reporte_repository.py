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
