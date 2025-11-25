from typing import List
from datetime import date
from src.Modules.Brigadas.Domain.integrante import IntegranteSalida
from src.Modules.Brigadas.Domain.integrante_repository import IntegranteRepository
from src.Modules.Ubicacion.Domain.departamento_repository import DepartamentoRepository
from src.Modules.Ubicacion.Application.departamento_listar_por_region import DepartamentoListarPorRegion


class IntegranteListarPorRegion:
    """
    Caso de uso para listar integrantes por región.
    Orquesta la lógica de obtener departamentos de una región y 
    luego buscar los integrantes correspondientes.
    """
    
    def __init__(
        self, 
        integrante_repository: IntegranteRepository,
        departamento_repository: DepartamentoRepository
    ):
        self.integrante_repository = integrante_repository
        self.departamento_repository = departamento_repository
    
    def execute(self, departamento_id: int, fecha_inicio: date, fecha_fin_aprox: date) -> List[IntegranteSalida]:
        """
        Ejecuta el caso de uso para listar integrantes por región.
        
        Args:
            departamento_id: ID del departamento de referencia para determinar la región
            fecha_inicio: Fecha de inicio solicitada
            fecha_fin_aprox: Fecha fin aproximada solicitada
            
        Returns:
            List[IntegranteSalida]: Lista de integrantes de la región
            
        Raises:
            ValueError: Si el departamento no existe o no se puede determinar la región
        """
        # Usar el caso de uso de departamentos para obtener los IDs de la región
        departamento_region_caso_uso = DepartamentoListarPorRegion(self.departamento_repository)
        ids_departamentos = departamento_region_caso_uso.obtener_ids_departamentos_region(departamento_id)
        
        if not ids_departamentos:
            raise ValueError(f"No se pudo determinar la región para el departamento {departamento_id}")
        
        # Obtener los integrantes usando el repositorio
        integrantes = self.integrante_repository.listar_por_region(ids_departamentos, fecha_inicio, fecha_fin_aprox)
        return integrantes