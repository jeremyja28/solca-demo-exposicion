import os
import sys

# Asegurar que se puede importar desde backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from backend.database import engine, his_engine, Base
from backend.models.usuario import Usuario
from sqlalchemy.orm import Session
import bcrypt

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def run_seed():
    print("Creando tabla de usuarios local si no existe...")
    Base.metadata.create_all(bind=engine)
    
    if not his_engine:
        print("⚠️ his_engine no está configurado (mock mode). Insertando médico de prueba...")
        default_password = get_password_hash("Solca2026*")
        with Session(engine) as session:
            if not session.query(Usuario).filter(Usuario.MedicoId == 10).first():
                session.add(Usuario(
                    Username="medico_10",
                    PasswordHash=default_password,
                    Nombre="DR. PRUEBA ONCOLOGO",
                    Rol="Doctor",
                    MedicoId=10,
                    Activo=True
                ))
                session.commit()
                print("✅ Médico de prueba insertado (Username: medico_10, Password: Solca2026*)")
        return

    print("Obteniendo médicos únicos de SOLCA (HIS)...")
    query = text("""
        SELECT Id, (Nombres + ' ' + Apellidos) AS Nombre, Especialidad
        FROM [dbo].[UsuariosSolcaT]
        WHERE Especialidad IS NOT NULL AND EsDoctor = 1
    """)
    
    try:
        with his_engine.connect() as conn:
            rows = conn.execute(query).mappings().all()
    except Exception as e:
        print(f"Error conectando a SQL Server: {e}")
        return

    if not rows:
        print("No se encontraron médicos en el HIS.")
        return

    print(f"Se encontraron {len(rows)} médicos. Insertando en BD local...")
    default_password = get_password_hash("Solca2026*")

    with Session(engine) as session:
        for row in rows:
            medico_id = row["Id"]
            nombre = row["Nombre"]
            especialidad = row["Especialidad"]
            
            # Generar username a partir del ID o el nombre
            username = f"medico_{medico_id}"
            
            # Verificar si ya existe
            existe = session.query(Usuario).filter(Usuario.MedicoId == medico_id).first()
            if not existe:
                nuevo_usuario = Usuario(
                    Username=username,
                    PasswordHash=default_password,
                    Nombre=nombre,
                    Rol="Doctor",
                    MedicoId=medico_id,
                    Activo=True
                )
                session.add(nuevo_usuario)
        
        session.commit()
        print("Sincronización de usuarios completada con éxito.")

if __name__ == "__main__":
    run_seed()
