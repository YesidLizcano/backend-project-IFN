from pydantic import BaseModel

class Municipio(BaseModel):
    nombre: str
    departamento_id: int

    class Config:
        from_attributes = True

class MunicipioSalida(Municipio):
    id: int
    pass
