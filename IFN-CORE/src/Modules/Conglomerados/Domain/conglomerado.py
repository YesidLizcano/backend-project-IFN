from datetime import date
from pydantic import BaseModel

from src.Modules.Conglomerados.Domain.subparcela import SubparcelaSalida


# --- 1. MODELO BASE (Componentes Comunes) ---
class ConglomeradoBase(BaseModel):
    """Contiene los campos comunes que el usuario provee."""
    fechaInicio: date
    fechaFinAprox: date
    fechaFin: date | None
    latitud: float
    longitud: float

# --- 2. DTO de CREACIÓN (Entrada de la API) ---
class ConglomeradoCrear(ConglomeradoBase):
    """
    Hereda los campos base. Se usa para el cuerpo del POST.
    NO lleva municipio_id ni id.
    """
    pass

# --- 2.1 DTO de ACTUALIZACIÓN DE FECHAS ---
class ConglomeradoActualizarFechas(BaseModel):
    """
    DTO para actualizar solo fechaInicio y fechaFinAprox.
    """
    fechaInicio: date
    fechaFinAprox: date

# --- 3. ENTIDAD DE DOMINIO ---
class Conglomerado(ConglomeradoBase):
    """
    Hereda los campos base y añade los campos CLAVE para la lógica
    que son obligatorios en el Dominio.
    """
    municipio_id: int 

# --- 4. DTO de SALIDA (Respuesta de la API) ---
class ConglomeradoSalida(Conglomerado):
    """
    Hereda la entidad de Dominio y añade los campos generados por la BD.
    """
    fechaInicio: date | None = None
    fechaFinAprox: date | None = None
    id: int
    subparcelas: list[SubparcelaSalida] = []

    class Config:
        from_attributes = True


# --- MODELOS PARA VERIFICACIÓN DE PUNTOS EN COLOMBIA ---
from typing import List

class PuntoCoords(BaseModel):
    lon: float
    lat: float

class VerificarPuntosRequest(BaseModel):
    puntos: List[PuntoCoords]

class VerificarPuntosResponse(BaseModel):
    resultados: List[bool]
