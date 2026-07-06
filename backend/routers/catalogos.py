from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.routers.auth import get_current_user
from backend.schemas.catalogo import EspecialidadOut, ActividadOut
from backend.database import get_db
from backend.models.complemento import Especialidad, Actividad

router = APIRouter()

@router.get("/especialidades", response_model=list[EspecialidadOut])
def get_especialidades(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Especialidad).filter(Especialidad.Activa == True).all()

@router.get("/actividades/{especialidad_id}", response_model=list[ActividadOut])
def get_actividades(especialidad_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Actividad).filter(
        Actividad.EspecialidadId == especialidad_id,
        Actividad.Activa == True).all()
