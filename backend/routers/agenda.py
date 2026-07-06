from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from backend.routers.auth import get_current_user
from backend.services.his_service import obtener_pacientes_his
from backend.services.merge_service import obtener_parte_diario_completo
from backend.schemas.parte_diario import RegistroParteDiario
from backend.database import get_db

router = APIRouter()

@router.get("/dia", response_model=list[RegistroParteDiario])
def get_agenda_dia(
    fecha: date = Query(default_factory=date.today),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["rol"] != "doctor":
        raise HTTPException(status_code=403, detail="Acceso exclusivo para médicos")

    medico_id = current_user["medico_id"]
    return obtener_parte_diario_completo(db, medico_id, fecha)

@router.get("/global", response_model=list[RegistroParteDiario])
def get_agenda_global(
    fecha_inicio: date = Query(default_factory=date.today),
    fecha_fin:    date = Query(default_factory=date.today),
    medico_id:    Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["rol"] != "enfermero":
        raise HTTPException(status_code=403, detail="Acceso exclusivo para enfermeros")
    
    # En mock retornamos todos por ahora
    import json
    with open("backend/data/mock_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    medicos = {p["MedicoId"] for p in data["pacientes"]}
    if medico_id:
        medicos = {medico_id}
        
    resultado = []
    for mid in medicos:
        # Simplificación para el mock, fecha_inicio/fin
        resultado.extend(obtener_parte_diario_completo(db, mid, fecha_inicio))
    
    return resultado
