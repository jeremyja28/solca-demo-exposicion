from pydantic import BaseModel
from typing import Optional

class ComplementoSchema(BaseModel):
    EspecialidadId : int
    ActividadId    : int
    TipoConsulta   : str
    Pre_QT         : bool
    Pre_QX         : bool
    Quimio         : bool
    EKG            : bool

class RegistroParteDiario(BaseModel):
    AgendamientoId   : int
    MedicoId         : int
    N_HC             : str
    Hora             : Optional[str] = None
    Apellidos        : str
    Nombres          : str
    FechaNacimiento  : str
    Edad             : int
    Sexo             : str
    CIE10            : Optional[str] = None
    Diagnostico      : Optional[str] = None
    Procedencia      : Optional[str] = None
    Convenio         : Optional[str] = None
    
    ComplementoCompleto : bool = False
    Complemento : Optional[ComplementoSchema] = None

    class Config:
        from_attributes = True
