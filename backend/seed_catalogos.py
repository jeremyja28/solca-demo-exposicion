import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import engine, Base
from backend.models.complemento import Especialidad, Actividad
from sqlalchemy.orm import Session

DATA_CATALOGOS = {
    "Oncología": [
        "ONCOLOGIA", 
        "QTA(QUIMIOTERAPIA AMBULATORIA)", 
        "QTH(QUIMIOTERAPIA HOSPITALARIA)", 
        "QTO(QUIMIOTERAPIA ORAL)", 
        "HT(HORMONOTERAPIA)"
    ],
    "Hematología y oncología": [
        "ONCOLOGIA", 
        "ONCO HEMATOLOGIA", 
        "HEMATOLOGIA", 
        "QTA(QUIMIOTERAPIA AMBULATORIA)", 
        "QTH(QUIMIOTERAPIA HOSPITALARIA)", 
        "QTO(QUIMIOTERAPIA ORAL)", 
        "HT(HORMONOTERAPIA)"
    ],
    "CIRUGIA ONCOLOGICA": [
        "CABEZA Y CUELLO", 
        "MAMA", 
        "MELANOMAS", 
        "GASTRICOS", 
        "TUMORES MIXTOS"
    ]
}

def run_seed_catalogos():
    print("Creando tablas si no existen...")
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        print("Limpiando datos actuales de Especialidades y Actividades...")
        session.query(Actividad).delete()
        session.query(Especialidad).delete()
        session.commit()

        print("Insertando catálogos...")
        for esp_nombre, actividades in DATA_CATALOGOS.items():
            esp = Especialidad(Nombre=esp_nombre, Activa=True)
            session.add(esp)
            session.flush() # Para obtener el ID

            for act_nombre in actividades:
                act = Actividad(EspecialidadId=esp.Id, Nombre=act_nombre, Activa=True)
                session.add(act)
        
        session.commit()
        print("Población de catálogos completada exitosamente.")

if __name__ == "__main__":
    run_seed_catalogos()
