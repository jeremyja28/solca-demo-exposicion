from pydantic import BaseModel
from typing import Literal
from datetime import date

class ComplementoInput(BaseModel):
    EspecialidadId : int
    ActividadId    : int
    TipoConsulta   : Literal["PRIMERA_VEZ", "SUBSECUENTE"]
    Pre_QT         : bool = False
    Pre_QX         : bool = False
    Quimio         : bool = False
    EKG            : bool = False

class ComplementoOutput(ComplementoInput):
    Id             : int
    AgendamientoId : int
    MedicoId       : int
    FechaParte     : date

    class Config:
        from_attributes = True
