from sqlalchemy import (
    Column, Integer, String, Boolean, Date,
    DateTime, ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Especialidad(Base):
    __tablename__ = "Especialidad"

    Id     = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(80), nullable=False, unique=True)
    Activa = Column(Boolean, nullable=False, default=True)

    actividades = relationship("Actividad", back_populates="especialidad")


class Actividad(Base):
    __tablename__ = "Actividad"

    Id             = Column(Integer, primary_key=True, autoincrement=True)
    EspecialidadId = Column(Integer, ForeignKey("Especialidad.Id"), nullable=False)
    Nombre         = Column(String(100), nullable=False)
    Activa         = Column(Boolean, nullable=False, default=True)

    especialidad = relationship("Especialidad", back_populates="actividades")


class ComplementoParteDiario(Base):
    __tablename__ = "Complemento_Parte_Diario"

    __table_args__ = (
        CheckConstraint(
            "TipoConsulta IN ('PRIMERA_VEZ', 'SUBSECUENTE')",
            name="ck_tipo_consulta"
        ),
        UniqueConstraint("AgendamientoId", name="uq_agendamiento"),
    )

    Id             = Column(Integer, primary_key=True, autoincrement=True)
    AgendamientoId = Column(Integer, nullable=False)
    MedicoId       = Column(Integer, nullable=False)
    FechaParte     = Column(Date,    nullable=False)
    EspecialidadId = Column(Integer, ForeignKey("Especialidad.Id"), nullable=False)
    ActividadId    = Column(Integer, ForeignKey("Actividad.Id"),    nullable=False)
    TipoConsulta   = Column(String(15), nullable=False)
    Pre_QT         = Column(Boolean, nullable=False, default=False)
    Pre_QX         = Column(Boolean, nullable=False, default=False)
    Quimio         = Column(Boolean, nullable=False, default=False)
    EKG            = Column(Boolean, nullable=False, default=False)
    CreadoEn       = Column(DateTime, server_default=func.now(), nullable=False)
    ActualizadoEn  = Column(DateTime, server_default=func.now(),
                            onupdate=func.now(), nullable=False)
    CreadoPor      = Column(Integer, nullable=False)

    especialidad = relationship("Especialidad")
    actividad    = relationship("Actividad")
