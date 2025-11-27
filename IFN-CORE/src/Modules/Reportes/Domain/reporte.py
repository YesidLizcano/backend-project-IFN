from pydantic import BaseModel
from typing import List, Any

class ReporteBase(BaseModel):
    nombre: str
    fecha_generacion: str
    datos: List[Any]

class ReporteInventario(ReporteBase):
    departamento: str
    total_items: int
