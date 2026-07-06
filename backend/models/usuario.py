from sqlalchemy import Column, Integer, String, Boolean
from backend.database import Base

class Usuario(Base):
    __tablename__ = "Usuarios"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String(50), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    Nombre = Column(String(100), nullable=False)
    Rol = Column(String(20), nullable=False, default="Doctor")
    MedicoId = Column(Integer, nullable=True) # ID del médico en HIS
    Activo = Column(Boolean, nullable=False, default=True)
