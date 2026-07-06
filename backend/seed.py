from backend.database import SessionLocal, engine
from backend.models.complemento import Especialidad, Actividad, Base

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    if db.query(Especialidad).count() > 0:
        print("Base de datos ya tiene datos. Omitiendo semilla.")
        db.close()
        return

    especialidades = [
        Especialidad(Nombre="Oncología Médica"),
        Especialidad(Nombre="Oncología Quirúrgica"),
        Especialidad(Nombre="Radioterapia"),
        Especialidad(Nombre="Hematología"),
        Especialidad(Nombre="Cardiología"),
        Especialidad(Nombre="Medicina Interna"),
    ]
    db.add_all(especialidades)
    db.commit()

    for e in especialidades:
        db.refresh(e)

    actividades = {
        "Oncología Médica":     ["Consulta nueva", "Consulta subsecuente",
                                 "Valoración pre-QT", "Valoración pre-QX",
                                 "Control de QT"],
        "Oncología Quirúrgica": ["Consulta nueva", "Consulta subsecuente",
                                 "Valoración pre-QX",
                                 "Seguimiento post-quirúrgico"],
        "Radioterapia":         ["Consulta nueva",
                                 "Planificación de tratamiento",
                                 "Seguimiento de tratamiento"],
        "Hematología":          ["Consulta nueva", "Consulta subsecuente",
                                 "Control de tratamiento"],
        "Cardiología":          ["Consulta nueva", "EKG",
                                 "Valoración pre-QT"],
        "Medicina Interna":     ["Consulta nueva", "Consulta subsecuente",
                                 "Interconsulta"],
    }

    esp_map = {e.Nombre: e.Id for e in especialidades}
    for nombre_esp, acts in actividades.items():
        for nombre_act in acts:
            db.add(Actividad(
                EspecialidadId=esp_map[nombre_esp],
                Nombre=nombre_act
            ))
    db.commit()
    db.close()
    print("Semilla aplicada correctamente.")

if __name__ == "__main__":
    seed()
