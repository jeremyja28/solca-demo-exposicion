import os
import shutil
from pathlib import Path

def crear_proyecto_demo():
    print("Iniciando empaquetado seguro del proyecto...")
    origen = Path(__file__).parent.resolve()
    destino = origen / "PROYECTO_DEMO_LIMPIO"

    # Si ya existe, eliminamos su contenido EXCEPTO .git
    if destino.exists():
        print(f"Limpiando directorio destino existente: {destino}")
        for item in destino.iterdir():
            if item.name != '.git':
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
    else:
        destino.mkdir(parents=True, exist_ok=True)

    # Definir qué ignorar
    carpetas_ignoradas = {
        '.git', 'node_modules', '__pycache__', '.venv', 'env', 'venv', 
        '.vscode', '.idea', 'PROYECTO_DEMO_LIMPIO', '.gemini'
    }
    
    archivos_ignorados_por_extension = {
        '.sqlite', '.sqlite3', '.db', '.xlsx', '.csv'
    }
    
    archivos_ignorados_especificos = {
        'test_conexion_solca.py', '.env'
    }

    def ignorar_archivos(directorio, archivos):
        ignorados = []
        for a in archivos:
            ruta_completa = Path(directorio) / a
            
            # Ignorar carpetas
            if ruta_completa.is_dir() and a in carpetas_ignoradas:
                ignorados.append(a)
                continue
                
            # Ignorar archivos específicos (ej. .env)
            if a in archivos_ignorados_especificos:
                ignorados.append(a)
                continue
                
            # Ignorar por extensión
            if ruta_completa.suffix.lower() in archivos_ignorados_por_extension:
                ignorados.append(a)
                continue
                
            # Ignorar cualquier archivo .env.* EXCEPTO .env.example
            if a.startswith('.env') and a != '.env.example':
                ignorados.append(a)
                continue
                
        return ignorados

    # Copiar recursivamente con las reglas de exclusión
    print("Copiando archivos, por favor espere...")
    shutil.copytree(origen, destino, ignore=ignorar_archivos, dirs_exist_ok=True)
    
    print("\n¡Empaquetado completado con éxito!")
    print(f"Tu proyecto limpio y seguro se encuentra en:\n{destino}")
    print("\nPor favor, verifica que la carpeta no contenga datos sensibles antes de publicar.")

if __name__ == "__main__":
    crear_proyecto_demo()
