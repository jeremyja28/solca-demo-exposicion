# Guía Definitiva de Pase a Producción - Sistema de Parte Diario (SOLCA)

Este documento contiene las instrucciones precisas para que el departamento de Infraestructura/IT despliegue el sistema en los servidores de producción del hospital.

## 1. Backend: Configuración de Base de Datos y Entorno

El sistema ha sido adaptado para funcionar nativamente con **PostgreSQL** en producción, manteniendo la conexión ODBC con el **SQL Server (HIS)**.

### 1.1 Dependencias Nuevas
Se ha actualizado el archivo `backend/requirements.txt` con los drivers requeridos:
- `psycopg2-binary==2.9.9` (Driver para PostgreSQL)
- `gunicorn==22.0.0` (Servidor WSGI de producción)

Para instalar todo:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # (En Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 1.2 Variables de Entorno (`.env`)
En producción, el archivo `backend/.env` debe lucir exactamente así:

```env
# Entorno
APP_ENV=production

# Base de datos transaccional local (PostgreSQL)
# Formato: postgresql://usuario:password@host:puerto/nombre_bd
DATABASE_URL=postgresql://postgres:tu_password_fuerte@localhost:5432/solca_parte_diario

# JWT Security
SECRET_KEY=tu_super_secreto_generado_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# HIS SQL Server (Modificar según credenciales reales)
HIS_DB_SERVER=webmedico-db-production-geo-rep.database.windows.net
HIS_DB_NAME=SwmDB_Production
HIS_DB_USER=UsuarioSolcaTDb
HIS_DB_PASSWORD=!SolcaT-Admin.*
HIS_DATA_SOURCE=sql
```

*(Nota de arquitectura: El código en `backend/database.py` y `Alembic` han sido pre-configurados para detectar la cadena `postgresql://` y omitir los flags exclusivos de SQLite automáticamente. No necesitas tocar código fuente).*

### 1.3 Creación de Tablas y Población de Datos Inicial (Ejecutar SOLO UNA VEZ)
Una vez configurado el `.env` con las credenciales de PostgreSQL vacía, ejecuta:

```bash
cd backend
# 1. Crear las tablas ejecutando las migraciones de Alembic
alembic upgrade head

# 2. Poblar los catálogos (Especialidades y Actividades)
python seed_catalogos.py

# 3. Sincronizar los médicos desde el HIS y crear usuarios
python seed_usuarios.py
```

### 1.4 Ejecutar el Backend en Producción
Se recomienda correr FastAPI bajo `Gunicorn` utilizando los workers de Uvicorn. Esto garantiza tolerancia a fallos y concurrencia.

```bash
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --daemon
```

---

## 2. Frontend: Compilación y Servidor Web

### 2.1 Compilación
El frontend (React/Vite) no se sube tal cual, sino que debe compilarse en archivos estáticos ligeros. En la máquina de desarrollo o servidor de CI/CD ejecuta:

```bash
cd frontend
npm install
npm run build
```
Esto generará una carpeta llamada `dist/`. Copia el contenido de esta carpeta al directorio público de tu servidor web (ej. `/var/www/solca-frontend`).

### 2.2 Configuración del Servidor Web (Nginx / Apache)
Dado que es una Single Page Application (SPA), el enrutamiento lo maneja React. Debes configurar tu servidor web para que **cualquier ruta no encontrada devuelva `index.html`** (Fallback routing).

**Ejemplo Nginx:**
```nginx
server {
    listen 80;
    server_name partediario.solca.ec;
    root /var/www/solca-frontend;
    index index.html;

    # Fallback para React Router
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Reverse Proxy para el API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Ejemplo Apache (`.htaccess` en la carpeta `dist/`):**
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

Con esto, el sistema estará robusto, escalable, con la base de datos de producción lista y corriendo en modo de alto rendimiento.
