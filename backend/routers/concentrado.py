from fastapi import APIRouter, Depends, Query, Response, HTTPException
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from backend.routers.auth import get_current_user
from backend.database import get_db
from backend.services.merge_service import obtener_parte_diario_completo
from backend.services.export_service import generar_concentrado_mensual

router = APIRouter()

@router.get("/mensual/exportar")
def exportar_concentrado_mensual(
    fecha_inicio: date = Query(default_factory=date.today),
    fecha_fin: date = Query(default_factory=date.today),
    medico_ids: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["rol"] != "enfermero":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    # Obtener IDs de médicos permitidos desde la tabla de Usuarios (sólo Doctores)
    from backend.models.usuario import Usuario
    doctores = db.query(Usuario).filter(Usuario.Rol == "Doctor").all()
    medicos_permitidos = {doc.MedicoId for doc in doctores if doc.MedicoId}
    
    if medico_ids:
        medicos = {int(x) for x in medico_ids.split(",")}
    else:
        medicos = medicos_permitidos
        
    registros = []
    for mid in medicos:
        registros.extend(obtener_parte_diario_completo(db, mid, fecha_inicio))
        
    xls_bytes = generar_concentrado_mensual(registros, fecha_inicio, fecha_fin)
    
    return Response(
        content=xls_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="Concentrado_{fecha_inicio}_{fecha_fin}.xlsx"'
        }
    )
