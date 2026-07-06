from typing import Optional
from sqlalchemy.orm import Session
from backend.models.complemento import ComplementoParteDiario
from backend.schemas.parte_diario import RegistroParteDiario, ComplementoSchema
from backend.services.his_service import obtener_pacientes_his, obtener_pacientes_his_mensual
import datetime
import re

def _limpiar_cie10(cie10_str) -> str:
    if not cie10_str:
        return ""
    # Split by semicolon, comma, or dash
    partes = re.split(r'[;,\-]', str(cie10_str))
    if partes:
        return partes[0].strip()
    return ""

def obtener_parte_diario_completo(
    db: Session,
    medico_id: int,
    fecha: datetime.date
) -> list[RegistroParteDiario]:
    pacientes_his = obtener_pacientes_his(medico_id=medico_id, fecha=fecha)
    
    if not pacientes_his:
        return []

    agendamiento_ids = [p["AgendamientoId"] for p in pacientes_his]

    complementos_raw = (
        db.query(ComplementoParteDiario)
        .filter(ComplementoParteDiario.AgendamientoId.in_(agendamiento_ids))
        .all()
    )

    complementos_dict: dict[int, ComplementoParteDiario] = {
        c.AgendamientoId: c for c in complementos_raw
    }

    resultado: list[RegistroParteDiario] = []

    for paciente in pacientes_his:
        ag_id = paciente["AgendamientoId"]
        complemento = complementos_dict.get(ag_id)

        registro = RegistroParteDiario(
            AgendamientoId   = ag_id,
            MedicoId         = paciente["MedicoId"],
            N_HC             = paciente["N_HC"],
            Apellidos        = paciente["APELLIDOS"],
            Nombres          = paciente["NOMBRES"],
            FechaNacimiento  = paciente["FECHA_NACIMIENTO"],
            Edad             = paciente["EDAD"],
            Sexo             = paciente["SEXO"],
            CIE10            = _limpiar_cie10(paciente.get("CIE10")),
            Diagnostico      = paciente["DIAGNOSTICO"],
            Procedencia      = paciente["PROCEDENCIA"],
            Convenio         = paciente["CONVENIO"],
            
            ComplementoCompleto = complemento is not None,
            
            Complemento = ComplementoSchema(
                EspecialidadId = complemento.EspecialidadId,
                ActividadId    = complemento.ActividadId,
                TipoConsulta   = complemento.TipoConsulta,
                Pre_QT         = complemento.Pre_QT,
                Pre_QX         = complemento.Pre_QX,
                Quimio         = complemento.Quimio,
                EKG            = complemento.EKG,
            ) if complemento else None
        )
        resultado.append(registro)

    return resultado


def obtener_parte_diario_mensual_completo(
    db: Session,
    medico_id: int,
    anio: int,
    mes: int
) -> list[RegistroParteDiario]:
    pacientes_his = obtener_pacientes_his_mensual(medico_id=medico_id, anio=anio, mes=mes)
    
    if not pacientes_his:
        return []

    agendamiento_ids = [p["AgendamientoId"] for p in pacientes_his]

    # Divide and conquer query if agendamiento_ids is too large, but usually a month for a doctor is ~500-1000 patients, which IN clause can handle.
    complementos_raw = (
        db.query(ComplementoParteDiario)
        .filter(ComplementoParteDiario.AgendamientoId.in_(agendamiento_ids))
        .all()
    )

    complementos_dict: dict[int, ComplementoParteDiario] = {
        c.AgendamientoId: c for c in complementos_raw
    }

    resultado: list[RegistroParteDiario] = []

    for paciente in pacientes_his:
        ag_id = paciente["AgendamientoId"]
        complemento = complementos_dict.get(ag_id)

        registro = RegistroParteDiario(
            AgendamientoId   = ag_id,
            MedicoId         = paciente["MedicoId"],
            N_HC             = paciente["N_HC"],
            Apellidos        = paciente["APELLIDOS"] if "APELLIDOS" in paciente else paciente.get("Apellidos", ""),
            Nombres          = paciente["NOMBRES"] if "NOMBRES" in paciente else paciente.get("Nombres", ""),
            FechaNacimiento  = paciente["FECHA_NACIMIENTO"] if "FECHA_NACIMIENTO" in paciente else paciente.get("FechaNacimiento", ""),
            Edad             = paciente["EDAD"] if "EDAD" in paciente else paciente.get("Edad", 0),
            Sexo             = paciente["SEXO"] if "SEXO" in paciente else paciente.get("Sexo", ""),
            CIE10            = _limpiar_cie10(paciente.get("CIE10")),
            Diagnostico      = paciente["DIAGNOSTICO"] if "DIAGNOSTICO" in paciente else paciente.get("Diagnostico", ""),
            Procedencia      = paciente["PROCEDENCIA"] if "PROCEDENCIA" in paciente else paciente.get("Procedencia", ""),
            Convenio         = paciente["CONVENIO"] if "CONVENIO" in paciente else paciente.get("Convenio", ""),
            
            ComplementoCompleto = complemento is not None,
            
            Complemento = ComplementoSchema(
                EspecialidadId = complemento.EspecialidadId,
                ActividadId    = complemento.ActividadId,
                TipoConsulta   = complemento.TipoConsulta,
                Pre_QT         = complemento.Pre_QT,
                Pre_QX         = complemento.Pre_QX,
                Quimio         = complemento.Quimio,
                EKG            = complemento.EKG,
            ) if complemento else None
        )
        
        # Guardaremos FechaAtencion temporalmente si lo necesitamos en el excel 
        # (pydantic model RegistroParteDiario doesnt have it natively, but we can set it dynamically or use it before returning)
        # Let's check if RegistroParteDiario supports dynamic attrs. Better not.
        # But wait, Plan Diario needs the exact date! 
        # I need to add FechaAtencion to the returned data, so I should modify RegistroParteDiario schema, or return tuples.
        # Let's modify RegistroParteDiario schema to include FechaAtencion.
        
        resultado.append((registro, paciente.get("FechaAtencion")))

    # Returning tuple of (registro, fecha_atencion) to avoid changing the schema and breaking other things.
    return resultado
