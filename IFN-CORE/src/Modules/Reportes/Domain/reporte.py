from pydantic import BaseModel
from typing import List, Any

class ReporteBase(BaseModel):
    nombre: str
    fecha_generacion: str
    datos: List[Any]

class ReporteInventario(ReporteBase):
    departamento: str
    total_items: int

class ReporteBrigadas(ReporteBase):
    total_brigadas: int

class ReporteConglomerados(ReporteBase):
    total_conglomerados: int

class ReporteEstadisticas(ReporteBase):
    total_conglomerados: int
    total_integrantes_activos_disponibles: int
    total_brigadas_activas: int

from datetime import date

class ConglomeradoDetalle(BaseModel):
    municipio: str
    fecha_inicio: date | None
    fecha_fin_aprox: date | None
    fecha_fin: date | None
    latitud: float
    longitud: float

class SubparcelaDetalle(BaseModel):
    latitud: float
    longitud: float

class BrigadaDetalle(BaseModel):
    fecha_creacion: date
    estado: str

class IntegranteDetalle(BaseModel):
    nombre: str
    rol: str
    telefono: str
    email: str

class MaterialDetalle(BaseModel):
    nombre: str
    cantidad_asignada: int

class ReporteInvestigacion(ReporteBase):
    conglomerado: ConglomeradoDetalle
    subparcelas: List[SubparcelaDetalle]
    brigada: BrigadaDetalle | None
    integrantes: List[IntegranteDetalle]
    materiales_equipos: List[MaterialDetalle]
