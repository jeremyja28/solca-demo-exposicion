from pydantic import BaseModel

class EspecialidadOut(BaseModel):
    Id: int
    Nombre: str

class ActividadOut(BaseModel):
    Id: int
    EspecialidadId: int
    Nombre: str
