import os
import sys
import json
import random
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

# Asegurar que podemos importar desde backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import engine, Base, SessionLocal
from backend.models.usuario import Usuario
from backend.models.complemento import Especialidad, Actividad
from backend.routers.auth import get_password_hash

# ==========================================
# CONFIGURACIÓN DE DATOS
# ==========================================

NOMBRES_M = ["LUIS", "JOSE", "CARLOS", "JUAN", "JORGE", "MARCO", "EDISON", "DIEGO", "ANGEL", "FABIAN", "MANUEL", "PEDRO"]
NOMBRES_F = ["MARIA", "ROSA", "CARMEN", "ANA", "BLANCA", "MARTHA", "GLADYS", "DIANA", "JESSICA", "ANDREA", "EVELYN", "SILVIA"]
APELLIDOS = ["ZAMBRANO", "SANCHEZ", "SALTOS", "VERA", "MENDOZA", "GARCIA", "CHAVEZ", "LOPEZ", "PEREZ", "RODRIGUEZ", "GONZALEZ", "FERNANDEZ", "ALVARADO", "CASTRO", "TORRES"]
CIUDADES = ["CUENCA", "AZOGUES", "LOJA", "MACAS", "MACHALA", "GUAYAQUIL", "QUITO"]
CONVENIOS = ["IESS", "MSP", "ISSPOL", "ISSFA", "PARTICULAR"]

ENFERMEDADES = [
    {"cie10": "C50.9", "diag": "TUMOR MALIGNO DE LA MAMA, PARTE NO ESPECIFICADA"},
    {"cie10": "E11.9", "diag": "DIABETES MELLITUS NO INSULINODEPENDIENTE, SIN MENCION DE COMPLICACION"},
    {"cie10": "I10.X", "diag": "HIPERTENSION ESENCIAL (PRIMARIA)"},
    {"cie10": "C61.X", "diag": "TUMOR MALIGNO DE LA PROSTATA"},
    {"cie10": "C16.9", "diag": "TUMOR MALIGNO DEL ESTOMAGO, PARTE NO ESPECIFICADA"},
    {"cie10": "E03.9", "diag": "HIPOTIROIDISMO, NO ESPECIFICADO"}
]

DOCTORES = [
    {
        "medico_id": 1,
        "username": "jose.aucapina",
        "nombre": "Dr. Jose Aucapiña",
        "rol": "Doctor",
        "especialidad": "ONCOLOGIA CLINICA",
        "actividades": ["ONCOLOGIA", "QTA(QUIMIOTERAPIA AMBULATORIA)", "QTH(QUIMIOTERAPIA HOSPITALARIA)", "QTO(QUIMIOTERAPIA ORAL)", "HT(HORMONOTERAPIA)"]
    },
    {
        "medico_id": 2,
        "username": "fabian.zamora",
        "nombre": "Dr. Fabian Zamora",
        "rol": "Doctor",
        "especialidad": "MEDICINA INTERNA",
        "actividades": ["PRE CONSULTA", "MEDICINA INTERNA", "CHEQUEO PRE QX", "CHEQUEO PRE QT"]
    },
    {
        "medico_id": 3,
        "username": "tatiana.martinez",
        "nombre": "Dra. Tatiana Martinez",
        "rol": "Doctor",
        "especialidad": "ENDOCRINOLOGIA",
        "actividades": []
    }
]

def generar_cedula():
    provincia = str(random.randint(1, 24)).zfill(2)
    resto = str(random.randint(10000000, 99999999))
    return provincia + resto

def generar_paciente(medico, fecha, hora_str):
    sexo_val = random.choice(["M", "F"])
    nombres_lista = NOMBRES_M if sexo_val == "M" else NOMBRES_F
    sexo_str = "Masculino" if sexo_val == "M" else "Femenino"
    
    nombres = f"{random.choice(nombres_lista)} {random.choice(nombres_lista)}"
    apellidos = f"{random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"
    
    edad = random.randint(30, 85)
    fecha_nac = fecha - timedelta(days=edad*365 + random.randint(0, 364))
    
    enf = random.choice(ENFERMEDADES)
    
    fecha_hora_cita = f"{fecha.isoformat()}T{hora_str}:00"
    
    return {
        "AgendamientoId": str(random.randint(10000, 99999)),
        "MedicoId": medico["medico_id"],
        "Hora": hora_str,
        "N_HC": generar_cedula(),
        "Apellidos": apellidos,
        "Nombres": nombres,
        "FechaNacimiento": fecha_nac.isoformat(),
        "Edad": edad,
        "Sexo": sexo_str,
        "CIE10": enf["cie10"],
        "Diagnostico": enf["diag"],
        "Procedencia": random.choice(CIUDADES),
        "Convenio": random.choice(CONVENIOS),
        "NombreDoctor": medico["nombre"].upper(),
        "EspecialidadDoctor": medico["especialidad"],
        "AreaConsultorio": medico["especialidad"], # CRÍTICO para autollenado
        "FechaHoraCita": fecha_hora_cita,
        "FechaAtencion": fecha.isoformat()
    }

def run():
    print("Iniciando generación de datos para DEMO PRODUCCIÓN...")
    
    # 1. Base de datos SQLite (Usuarios, Especialidad, Actividad)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    
    try:
        # Limpiar
        print("Vaciando tablas...")
        session.query(Usuario).delete()
        session.query(Actividad).delete()
        session.query(Especialidad).delete()
        session.commit()
        
        # Insertar Usuarios
        print("Creando usuarios...")
        password = "Demo2026*"
        hashed_pwd = get_password_hash(password)
        
        # Enfermeria
        session.add(Usuario(
            Username="enfermeria_admin",
            PasswordHash=hashed_pwd,
            Nombre="Enfermeria",
            Rol="Enfermero",
            MedicoId=None,
            Activo=True
        ))
        
        # Doctores y Especialidades
        for doc in DOCTORES:
            # Usuario
            session.add(Usuario(
                Username=doc["username"],
                PasswordHash=hashed_pwd,
                Nombre=doc["nombre"],
                Rol=doc["rol"],
                MedicoId=doc["medico_id"],
                Activo=True
            ))
            
            # Especialidad
            esp = Especialidad(Nombre=doc["especialidad"], Activa=True)
            session.add(esp)
            session.flush() # Para obtener el ID
            
            # Actividades
            for act_name in doc["actividades"]:
                session.add(Actividad(
                    EspecialidadId=esp.Id,
                    Nombre=act_name,
                    Activa=True
                ))
                
        session.commit()
        print("Usuarios y catálogos creados exitosamente.")
        
    except Exception as e:
        session.rollback()
        print(f"Error en la base de datos: {e}")
        return
    finally:
        session.close()
        
    # 2. Generar mock_data.json
    print("Generando pacientes simulados...")
    hoy = date.today()
    manana = hoy + timedelta(days=1)
    fechas = [hoy, manana]
    
    horas = ["08:00", "08:45", "09:30", "10:15", "11:00", "11:45", "12:30", "13:15", "14:00", "14:45"]
    pacientes_list = []
    
    for f in fechas:
        for doc in DOCTORES:
            for h in horas:
                pacientes_list.append(generar_paciente(doc, f, h))
                
    mock_data = {"pacientes": pacientes_list}
    
    ruta_mock = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "data", "mock_data.json")
    
    # Crear directorio si no existe (por si acaso)
    os.makedirs(os.path.dirname(ruta_mock), exist_ok=True)
    
    with open(ruta_mock, "w", encoding="utf-8") as f:
        json.dump(mock_data, f, ensure_ascii=False, indent=2)
        
    print(f"Se han generado {len(pacientes_list)} pacientes en {ruta_mock}")
    print("Generación DEMO finalizada con éxito!")

if __name__ == "__main__":
    run()
