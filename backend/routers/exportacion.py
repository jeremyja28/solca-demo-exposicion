from fastapi import APIRouter, Depends, Query, Response, HTTPException
from datetime import date
from sqlalchemy.orm import Session
from backend.routers.auth import get_current_user
from backend.database import get_db
from backend.services.merge_service import obtener_parte_diario_completo, obtener_parte_diario_mensual_completo
from backend.services.export_service import generar_pdf_parte_diario, generar_excel_parte_diario, generar_excel_concentrado_mensual

router = APIRouter()

@router.get("/pdf")
def exportar_pdf(
    fecha: date = Query(default_factory=date.today),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    medico_id = current_user["medico_id"]
    registros = obtener_parte_diario_completo(db, medico_id, fecha)
    pdf_bytes = generar_pdf_parte_diario(
        registros,
        medico_nombre=current_user.get("sub", f"Dr. {medico_id}"),
        fecha=fecha
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="ParteDiario_{fecha}.pdf"'
        }
    )

@router.get("/excel")
def exportar_excel(
    fecha: date = Query(default_factory=date.today),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    medico_id = current_user["medico_id"]
    registros = obtener_parte_diario_completo(db, medico_id, fecha)
    xls_bytes = generar_excel_parte_diario(
        registros,
        medico_nombre=current_user.get("sub", f"Dr. {medico_id}"),
        fecha=fecha
    )
    return Response(
        content=xls_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="ParteDiario_{fecha}.xlsx"'
        }
    )


@router.get("/excel/{medico_id}")
def exportar_excel_mensual(
    medico_id: int,
    mes: int = Query(..., description="Mes del reporte (1-12)"),
    anio: int = Query(..., description="Año del reporte"),
    db: Session = Depends(get_db)
):
    # En un entorno real se debería verificar que current_user tenga permisos para ver este médico, 
    # pero aquí implementamos la ruta tal cual se solicitó.
    registros_tuplas = obtener_parte_diario_mensual_completo(db, medico_id, anio, mes)
    
    # Nombre de médico por defecto si no tenemos el dato (idealmente vendría de la DB)
    medico_nombre = f"Dr. {medico_id}"
    
    xls_bytes = generar_excel_concentrado_mensual(
        registros_tuplas,
        medico_nombre=medico_nombre,
        anio=anio,
        mes=mes
    )
    
    return Response(
        content=xls_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="ConcentradoMensual_{anio}_{mes:02d}.xlsx"'
        }
    )


@router.get("/diario/pdf/{medico_id}")
def exportar_diario_pdf_por_medico(
    medico_id: int,
    fecha: date = Query(default_factory=date.today),
    db: Session = Depends(get_db)
):
    registros = obtener_parte_diario_completo(db, medico_id, fecha)
    if not registros:
        raise HTTPException(status_code=404, detail="No hay pacientes atendidos en esta fecha para generar el reporte.")
        
    medico_nombre = f"Dr. {medico_id}"
    pdf_bytes = generar_pdf_parte_diario(registros, medico_nombre=medico_nombre, fecha=fecha)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="ParteDiario_{fecha}.pdf"'
        }
    )

@router.get("/diario/excel/{medico_id}")
def exportar_diario_excel_por_medico(
    medico_id: int,
    fecha: date = Query(default_factory=date.today),
    db: Session = Depends(get_db)
):
    registros = obtener_parte_diario_completo(db, medico_id, fecha)
    if not registros:
        raise HTTPException(status_code=404, detail="No hay pacientes atendidos en esta fecha para generar el reporte.")
        
    medico_nombre = f"Dr. {medico_id}"
    xls_bytes = generar_excel_parte_diario(registros, medico_nombre=medico_nombre, fecha=fecha)
    
    return Response(
        content=xls_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="ParteDiario_{fecha}.xlsx"'
        }
    )
