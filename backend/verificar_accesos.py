import os
import sys

# Asegurar que se puede importar desde backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import engine
from backend.models.usuario import Usuario
from sqlalchemy.orm import Session
import bcrypt

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_y_crear():
    default_password_plain = "Solca2026*"
    default_password_hash = get_password_hash(default_password_plain)

    with Session(engine) as session:
        # 1. Crear usuario de enfermería si no existe
        enfermero = session.query(Usuario).filter(Usuario.Username == "enfermeria_admin").first()
        if not enfermero:
            nuevo_enfermero = Usuario(
                Username="enfermeria_admin",
                PasswordHash=default_password_hash,
                Nombre="Administrador de Enfermería",
                Rol="enfermero", # Asegurar que coincide con lo que espera el router
                Activo=True
            )
            session.add(nuevo_enfermero)
            session.commit()
            print("[+] Usuario 'enfermeria_admin' creado con éxito.\n")
        else:
            print("[i] El usuario 'enfermeria_admin' ya existe. Omitiendo creación.\n")

        # 2. Consultar y mostrar los primeros 10 doctores y al enfermero
        print("=== AUDITORÍA DE ACCESOS ===")
        print(f"{'ID':<5} | {'USERNAME':<20} | {'NOMBRE COMPLETO':<40} | {'ROL':<15}")
        print("-" * 87)

        # Buscar al enfermero (o enfermeros)
        enfermeros = session.query(Usuario).filter(Usuario.Rol == "enfermero").all()
        for e in enfermeros:
            print(f"{e.Id:<5} | {e.Username:<20} | {e.Nombre:<40} | {e.Rol:<15}")
        
        print("-" * 87)

        # Buscar primeros 10 doctores
        doctores = session.query(Usuario).filter(Usuario.Rol == "Doctor").limit(10).all()
        for d in doctores:
            print(f"{d.Id:<5} | {d.Username:<20} | {d.Nombre[:38]:<40} | {d.Rol:<15}")

        print("-" * 87)
        print(f"Total de médicos en base de datos: {session.query(Usuario).filter(Usuario.Rol == 'Doctor').count()}")
        print(f"Contraseña por defecto para todos: {default_password_plain}")

if __name__ == "__main__":
    verificar_y_crear()
