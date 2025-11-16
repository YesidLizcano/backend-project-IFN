from pydantic import BaseModel


class Subparcela(BaseModel):
    conglomerado_id: int | None = None
    latitud: float
    longitud: float

class SubparcelaSalida(Subparcela):
    id: int
    pass

    class Config:
        from_attributes = True