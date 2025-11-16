from typing import List, Optional
from src.Shared.Domain.departamento import DepartamentoSalida
from src.Shared.Domain.departamento_repository import DepartamentoRepository


class DepartamentoListarPorRegion:
    """
    Caso de uso para obtener departamentos por región.
    Maneja la lógica de clasificación regional de Colombia.
    """
    
    # Mapa de regiones de Colombia
    REGIONES = {
        "Andina": ["ANTIOQUIA", "BOYACÁ", "CALDAS", "CUNDINAMARCA", "HUILA", "NARIÑO", 
                   "NORTE DE SANTANDER", "QUINDÍO", "RISARALDA", "SANTANDER", "TOLIMA"],
        "Caribe": ["ATLÁNTICO", "BOLÍVAR", "CESAR", "CÓRDOBA", "LA GUAJIRA", "MAGDALENA", 
                   "SUCRE", "SAN ANDRÉS Y PROVIDENCIA"],
        "Pacífica": ["CHOCÓ", "VALLE DEL CAUCA", "CAUCA", "NARIÑO"],
        "Orinoquía": ["ARAUCA", "CASANARE", "META", "VICHADA"],
        "Amazónica": ["AMAZONAS", "CAQUETÁ", "GUAVIARE", "GUAINÍA", "PUTUMAYO", "VAUPÉS"]
    }

    def __init__(self, departamento_repository: DepartamentoRepository):
        self.departamento_repository = departamento_repository

    def obtener_departamentos_de_region(self, nombre_region: str) -> List[str]:
        """
        Obtiene todos los departamentos que pertenecen a una región específica.
        
        Args:
            nombre_region: Nombre de la región
            
        Returns:
            List[str]: Lista de nombres de departamentos de la región
        """
        return self.REGIONES.get(nombre_region, [])

    def obtener_nombre_region(self, nombre_departamento: str) -> Optional[str]:
        """
        Obtiene el nombre de la región a la que pertenece el departamento.
        
        Args:
            nombre_departamento: Nombre del departamento
            
        Returns:
            str: Nombre de la región, o None si no se encuentra
        """
        nombre_depto_upper = nombre_departamento.upper()
        
        for region, departamentos in self.REGIONES.items():
            if nombre_depto_upper in departamentos:
                return region
        
        return None

    def obtener_ids_departamentos_region(self, departamento_id: int) -> List[int]:
        """
        Obtiene los IDs de todos los departamentos que pertenecen a la misma región 
        que el departamento especificado.
        
        Args:
            departamento_id: ID del departamento de referencia
            
        Returns:
            List[int]: Lista de IDs de departamentos de la región
        """
        # Obtener el departamento
        departamento = self.departamento_repository.buscar_por_id(departamento_id)
        if not departamento:
            raise ValueError(f"Departamento con ID {departamento_id} no encontrado")
        
        # Obtener la región del departamento
        region = self.obtener_nombre_region(departamento.nombre)
        if not region:
            raise ValueError(f"Región para el departamento {departamento.nombre} no encontrada")
        
        # Obtener todos los departamentos de la región
        departamentos_region = self.obtener_departamentos_de_region(region)
        
        # Obtener los IDs de estos departamentos
        ids_departamentos = []
        departamentos_objetos = self.departamento_repository.listar_departamentos()
        
        for depto in departamentos_objetos:
            if depto.nombre.upper() in departamentos_region:
                ids_departamentos.append(depto.id)
        
        return ids_departamentos