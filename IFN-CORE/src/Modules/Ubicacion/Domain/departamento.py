from pydantic import BaseModel

class Departamento(BaseModel):
    nombre: str

class DepartamentoSalida(Departamento):
    id: int
    pass

    class Config:
        from_attributes = True

