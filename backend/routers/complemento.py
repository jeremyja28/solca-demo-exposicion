from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from backend.routers.auth import get_current_user
from backend.database import get_db
from backend.models.complemento import ComplementoParteDiario
from backend.schemas.complemento import ComplementoInput, ComplementoOutput
from backend.services.his_service import obtener_pacientes_his

router = APIRouter()

@router.put("/{agendamiento_id}", response_model=ComplementoOutput)
def upsert_complemento(
    agendamiento_id: int,
    payload: ComplementoInput,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["rol"] != "doctor":
        raise HTTPException(status_code=403, detail="Solo médicos pueden completar el parte diario")

    medico_id = current_user["medico_id"]
    pacientes = obtener_pacientes_his(medico_id, date.today())
    ids_propios = {p["AgendamientoId"] for p in pacientes}

    if agendamiento_id not in ids_propios:
        raise HTTPException(status_code=403, detail="Este agendamiento no pertenece al médico autenticado")

    existente = db.query(ComplementoParteDiario).filter_by(AgendamientoId=agendamiento_id).first()

    if existente:
        for campo, valor in payload.model_dump().items():
            setattr(existente, campo, valor)
        registro = existente
    else:
        registro = ComplementoParteDiario(
            AgendamientoId = agendamiento_id,
            MedicoId       = medico_id,
            FechaParte     = date.today(),
            CreadoPor      = int(current_user["sub"]),
            **payload.model_dump()
        )
        db.add(registro)

    db.commit()
    db.refresh(registro)
    
    # Adaptar para que FechaParte devuelva un string
    result = ComplementoOutput.model_validate(registro)
    result.FechaParte = str(registro.FechaParte)
    return result
