# 03 — Plan de Implementación
## Sistema de Parte Diario Médico — SOLCA

> **Versión:** 1.0  
> **Fecha:** Junio 2026  
> **Estado:** Aprobado para ejecución  
> **Dependencias:** `01_Requisitos_y_Casos_Uso.md` · `02_Arquitectura_y_Base_Datos.md`  
> **Metodología:** Scrum adaptado — sprints de 1 semana

---

## Resumen Ejecutivo

| Fase | Nombre | Duración | Entregable principal |
|---|---|---|---|
| **1** | Backend · Entorno y lectura de datos | 1 semana | API funcional con mock, endpoints GET protegidos por JWT |
| **2** | Backend · Escritura y persistencia local | 1 semana | Endpoints PUT/UPSERT sobre SQLite, BD local operativa |
| **3** | Frontend · Vistas Doctor y Enfermero | 1–2 semanas | UI completa integrada con el backend, colores SOLCA |
| **4** | Reportes y conexión SQL Server real | 1 semana | PDF/Excel, Concentrado Mensual, migración desde mock |

**Duración total estimada:** 4–5 semanas  
**Equipo mínimo recomendado:** 1 desarrollador backend Python · 1 desarrollador frontend · 1 QA / tester funcional

---

## Convenciones del documento

- `[ ]` Tarea pendiente
- `[x]` Tarea completada (marcar durante la ejecución)
- **⚠ Bloqueante:** si esta tarea no se completa, las siguientes no pueden comenzar
- **✎ Criterio de aceptación:** condición verificable para dar la tarea por cerrada

---

---

# FASE 1 — Backend: Entorno, Mock Data y Endpoints de Lectura

**Objetivo:** Tener un servidor Python corriendo localmente que exponga los datos del HIS (desde `mock_data.json`) a través de una API REST protegida, filtrada por `MedicoId` extraído del JWT.

**Duración:** 5 días hábiles  
**Rama Git:** `feature/fase-1-backend-lectura`

---

## Día 1 — Configuración del entorno Python

### Tarea 1.1 — Crear estructura del proyecto

```
[ ] Crear repositorio Git con rama main y develop
[ ] Crear carpeta raíz: solca-parte-diario/
[ ] Crear subcarpeta: backend/
[ ] Inicializar entorno virtual Python 3.11+:
        python -m venv .venv
        source .venv/bin/activate   (Linux/Mac)
        .venv\Scripts\activate      (Windows)
```

### Tarea 1.2 — Instalar dependencias base

```
[ ] Crear backend/requirements.txt con el siguiente contenido:

        fastapi==0.111.0
        uvicorn[standard]==0.29.0
        python-jose[cryptography]==3.3.0
        passlib[bcrypt]==1.7.4
        pydantic==2.7.1
        pydantic-settings==2.2.1
        sqlalchemy==2.0.30
        alembic==1.13.1
        python-multipart==0.0.9
        httpx==0.27.0          # para tests de la API

[ ] Instalar dependencias:
        pip install -r requirements.txt

[ ] Verificar instalación:
        python -c "import fastapi; print(fastapi.__version__)"
```

✎ **Criterio de aceptación:** el comando de verificación imprime la versión sin errores.

### Tarea 1.3 — Crear estructura de carpetas del backend

```
[ ] Crear los siguientes archivos vacíos con su estructura:

    backend/
    ├── main.py
    ├── config.py
    ├── database.py
    ├── models/
    │   └── __init__.py
    ├── schemas/
    │   └── __init__.py
    ├── routers/
    │   └── __init__.py
    ├── services/
    │   └── __init__.py
    └── data/
        └── (vacío por ahora)
```

### Tarea 1.4 — Configurar variables de entorno

```
[ ] Crear archivo backend/.env con el contenido de la Sección 8
    del documento 02_Arquitectura_y_Base_Datos.md

[ ] Crear backend/config.py:

        from pydantic_settings import BaseSettings

        class Settings(BaseSettings):
            APP_ENV: str = "development"
            DATABASE_URL: str = "sqlite:///./solca_parte_diario.db"
            SECRET_KEY: str = "dev-secret-key"
            ALGORITHM: str = "HS256"
            ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
            HIS_DATA_SOURCE: str = "mock"

            class Config:
                env_file = ".env"

        settings = Settings()

[ ] Agregar .env al .gitignore (nunca subir credenciales al repo)
```

✎ **Criterio de aceptación:** `from backend.config import settings; print(settings.APP_ENV)` imprime `development`.

---

## Día 2 — Mock Data y servidor base

### Tarea 2.1 — Crear `mock_data.json`

```
[ ] Copiar la estructura JSON completa definida en la Sección 4.2
    del documento 02_Arquitectura_y_Base_Datos.md en:
    backend/data/mock_data.json

[ ] Verificar que el JSON es válido:
        python -c "import json; json.load(open('backend/data/mock_data.json'))"
        # Debe terminar sin errores

[ ] Confirmar que los 6 registros están distribuidos entre
    MedicoId: 10 (3 pacientes), 11 (2 pacientes), 12 (1 paciente)
```

✎ **Criterio de aceptación:** el JSON es válido y contiene los campos `AgendamientoId` y `MedicoId` en cada registro.

### Tarea 2.2 — Crear el servidor FastAPI base

```
[ ] Crear backend/main.py:

        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware

        app = FastAPI(
            title="SOLCA - Parte Diario Médico",
            version="1.0.0",
            docs_url="/api/docs",
            redoc_url="/api/redoc"
        )

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000",
                           "http://localhost:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/health")
        def health_check():
            return {"status": "ok", "sistema": "SOLCA Parte Diario"}

[ ] Levantar el servidor:
        uvicorn backend.main:app --reload --port 8000

[ ] Verificar en el navegador: http://localhost:8000/health
[ ] Verificar documentación automática:  http://localhost:8000/api/docs
```

⚠ **Bloqueante:** el servidor debe estar corriendo antes de continuar.

✎ **Criterio de aceptación:** `GET /health` retorna `{"status": "ok", ...}` con código HTTP 200.

---

## Día 3 — Autenticación JWT

### Tarea 3.1 — Crear usuarios de prueba (hardcoded para Fase 1)

```
[ ] Crear backend/data/usuarios_dev.json:

        {
          "usuarios": [
            {
              "id": 10,
              "username": "dr.gutierrez",
              "password_hash": "$2b$12$...",
              "rol": "doctor",
              "nombre_completo": "Dr. Carlos Gutiérrez",
              "medico_id": 10
            },
            {
              "id": 11,
              "username": "dr.paredes",
              "password_hash": "$2b$12$...",
              "rol": "doctor",
              "nombre_completo": "Dra. María Paredes",
              "medico_id": 11
            },
            {
              "id": 20,
              "username": "enf.torres",
              "password_hash": "$2b$12$...",
              "rol": "enfermero",
              "nombre_completo": "Lcda. Rosa Torres",
              "medico_id": null
            }
          ]
        }

[ ] Generar los hashes de contraseña de prueba:
        from passlib.context import CryptContext
        pwd = CryptContext(schemes=["bcrypt"])
        print(pwd.hash("Solca2026!"))
        # Reemplazar los "$2b$12$..." del JSON con el hash generado
```

### Tarea 3.2 — Implementar endpoint de login

```
[ ] Crear backend/routers/auth.py con:
    - Función verify_password(plain, hashed)
    - Función create_access_token(data: dict) → str (JWT)
    - Función get_current_user(token) → dict  (dependencia FastAPI)
    - POST /auth/login  →  recibe username/password, retorna JWT

[ ] El payload del JWT debe contener:
        {
          "sub": "10",          ← id del usuario
          "rol": "doctor",
          "medico_id": 10,      ← null si es enfermero
          "exp": <timestamp>
        }

[ ] Registrar el router en main.py:
        from backend.routers import auth
        app.include_router(auth.router, prefix="/auth", tags=["Auth"])
```

✎ **Criterio de aceptación:** `POST /auth/login` con credenciales correctas retorna un token JWT válido. Con credenciales incorrectas retorna HTTP 401.

---

## Día 4 — Servicio HIS y endpoint de agenda

### Tarea 4.1 — Implementar `his_service.py`

```
[ ] Crear backend/services/his_service.py con la función
    obtener_pacientes_his(medico_id, fecha) definida en
    la Sección 5.4 del documento 02_Arquitectura_y_Base_Datos.md

[ ] La función debe:
    - Leer backend/data/mock_data.json
    - Filtrar por medico_id
    - Retornar lista de dicts con todos los campos del JSON
    - Retornar lista vacía (no error) si no hay coincidencias
```

### Tarea 4.2 — Crear schemas Pydantic de lectura

```
[ ] Crear backend/schemas/parte_diario.py con:
    - class ComplementoSchema (campos opcionales todos)
    - class RegistroParteDiario (campos HIS + ComplementoCompleto + Complemento)
    definidos en la Sección 5.3 del documento 02_Arquitectura_y_Base_Datos.md

[ ] Crear backend/schemas/catalogo.py con:

        class EspecialidadOut(BaseModel):
            Id: int
            Nombre: str

        class ActividadOut(BaseModel):
            Id: int
            EspecialidadId: int
            Nombre: str
```

### Tarea 4.3 — Crear endpoint `GET /agenda/dia`

```
[ ] Crear backend/routers/agenda.py:

        @router.get("/dia", response_model=list[RegistroParteDiario])
        def get_agenda_dia(
            fecha: date = Query(default=date.today()),
            current_user: dict = Depends(get_current_user)
        ):
            if current_user["rol"] != "doctor":
                raise HTTPException(status_code=403,
                    detail="Acceso exclusivo para médicos")

            medico_id = current_user["medico_id"]
            pacientes = obtener_pacientes_his(medico_id, fecha)

            # En Fase 1 no hay BD local aún; Complemento siempre null
            return [
                RegistroParteDiario(**p, ComplementoCompleto=False, Complemento=None)
                for p in pacientes
            ]

[ ] Registrar el router en main.py con prefix="/agenda"
```

✎ **Criterio de aceptación:**
- `GET /agenda/dia` sin token → HTTP 401.
- `GET /agenda/dia` con token del `dr.gutierrez` (MedicoId=10) → retorna exactamente 3 pacientes.
- `GET /agenda/dia` con token del `dr.paredes` (MedicoId=11) → retorna exactamente 2 pacientes.
- Un médico nunca recibe pacientes de otro médico.

---

## Día 5 — Endpoint de catálogos y pruebas de Fase 1

### Tarea 5.1 — Endpoint de catálogos (Especialidad y Actividad)

```
[ ] Crear backend/data/catalogos_dev.json con la lista de
    especialidades y actividades del Sección 3.2 del documento
    02_Arquitectura_y_Base_Datos.md (datos semilla en JSON
    para no depender de la BD aún)

[ ] Crear backend/routers/catalogos.py:
    - GET /catalogos/especialidades  → lista de especialidades activas
    - GET /catalogos/actividades/{especialidad_id}  → actividades de esa especialidad
    Ambos requieren JWT válido (cualquier rol)

[ ] Registrar el router en main.py
```

### Tarea 5.2 — Pruebas manuales de Fase 1

```
[ ] Probar todos los endpoints desde la UI de Swagger:
    http://localhost:8000/api/docs

    Checklist de pruebas:
    [ ] POST /auth/login  con credenciales correctas → 200 + JWT
    [ ] POST /auth/login  con clave incorrecta → 401
    [ ] GET  /agenda/dia  sin token → 401
    [ ] GET  /agenda/dia  con token doctor MedicoId=10 → 3 registros
    [ ] GET  /agenda/dia  con token doctor MedicoId=11 → 2 registros
    [ ] GET  /agenda/dia  con token doctor MedicoId=12 → 1 registro
    [ ] GET  /catalogos/especialidades → lista de 6+ especialidades
    [ ] GET  /catalogos/actividades/1  → actividades de Oncología Médica
    [ ] GET  /catalogos/actividades/99 → lista vacía (sin error 500)
```

### Tarea 5.3 — Cierre de Fase 1

```
[ ] Hacer commit con mensaje: "feat: fase-1 - API lectura mock con JWT"
[ ] Crear Pull Request de feature/fase-1 → develop
[ ] Actualizar README.md con instrucciones de arranque del servidor
[ ] Documentar contraseñas de prueba en documento interno (nunca en Git)
```

⚠ **Bloqueante para Fase 2:** todos los endpoints de lectura deben pasar el checklist de pruebas antes de iniciar la siguiente fase.

---

---

# FASE 2 — Backend: Base de Datos Local y Endpoints de Escritura

**Objetivo:** Crear la BD local (SQLite), implementar el UPSERT del complemento del médico y entregar el JOIN en memoria entre el HIS y la BD local.

**Duración:** 5 días hábiles  
**Rama Git:** `feature/fase-2-backend-escritura`

---

## Día 6 — Configuración de SQLAlchemy y SQLite

### Tarea 6.1 — Configurar la conexión a la BD

```
[ ] Crear backend/database.py:

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker, DeclarativeBase
        from backend.config import settings

        engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False}  # Solo SQLite
        )

        SessionLocal = sessionmaker(autocommit=False,
                                    autoflush=False,
                                    bind=engine)

        class Base(DeclarativeBase):
            pass

        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
```

### Tarea 6.2 — Crear los modelos ORM

```
[ ] Crear backend/models/complemento.py con los modelos
    Especialidad, Actividad y ComplementoParteDiario
    definidos en la Sección 3.3 del documento 02_Arquitectura_y_Base_Datos.md

[ ] Crear backend/models/__init__.py que importe todos los modelos
    (necesario para que Alembic los detecte)
```

### Tarea 6.3 — Inicializar Alembic y crear la migración inicial

```
[ ] Inicializar Alembic:
        alembic init backend/migrations

[ ] Editar backend/migrations/env.py:
    - Importar Base desde backend.database
    - Importar todos los modelos desde backend.models
    - Configurar target_metadata = Base.metadata

[ ] Editar alembic.ini:
    - Cambiar sqlalchemy.url para que lea de config.py:
        sqlalchemy.url =    ← dejar vacío, se toma del env.py

[ ] Generar la migración inicial:
        alembic revision --autogenerate -m "crear_tablas_iniciales"

[ ] Revisar el archivo generado en backend/migrations/versions/
    y confirmar que crea las 3 tablas:
    Especialidad, Actividad, Complemento_Parte_Diario

[ ] Aplicar la migración:
        alembic upgrade head

[ ] Verificar que el archivo solca_parte_diario.db fue creado
```

✎ **Criterio de aceptación:** `alembic current` muestra la migración como aplicada. El archivo `.db` existe en disco.

---

## Día 7 — Datos semilla y servicio de catálogos desde BD

### Tarea 7.1 — Script de semilla de catálogos

```
[ ] Crear backend/seed.py:

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

            # Refrescar para obtener los IDs asignados
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

[ ] Ejecutar el script:
        python -m backend.seed

[ ] Verificar que se crearon 6 especialidades y las actividades
    correspondientes en la BD
```

### Tarea 7.2 — Migrar catálogos de JSON a BD en el router

```
[ ] Actualizar backend/routers/catalogos.py para que ahora
    lea desde la BD (SQLAlchemy) en lugar del JSON:

        @router.get("/especialidades",
                    response_model=list[EspecialidadOut])
        def get_especialidades(db: Session = Depends(get_db),
                               _=Depends(get_current_user)):
            return db.query(Especialidad).filter(
                Especialidad.Activa == True).all()

        @router.get("/actividades/{especialidad_id}",
                    response_model=list[ActividadOut])
        def get_actividades(especialidad_id: int,
                            db: Session = Depends(get_db),
                            _=Depends(get_current_user)):
            return db.query(Actividad).filter(
                Actividad.EspecialidadId == especialidad_id,
                Actividad.Activa == True).all()
```

✎ **Criterio de aceptación:** `GET /catalogos/actividades/1` retorna las 5 actividades de Oncología Médica desde la BD.

---

## Día 8 — Schema de entrada y endpoint PUT complemento

### Tarea 8.1 — Schema Pydantic de escritura

```
[ ] Crear backend/schemas/complemento.py:

        from pydantic import BaseModel, field_validator
        from typing import Literal

        class ComplementoInput(BaseModel):
            EspecialidadId : int
            ActividadId    : int
            TipoConsulta   : Literal["PRIMERA_VEZ", "SUBSECUENTE"]
            Pre_QT         : bool = False
            Pre_QX         : bool = False
            Quimio         : bool = False
            EKG            : bool = False

        class ComplementoOutput(ComplementoInput):
            Id             : int
            AgendamientoId : int
            MedicoId       : int
            FechaParte     : str

            class Config:
                from_attributes = True
```

### Tarea 8.2 — Endpoint `PUT /complemento/{agendamiento_id}`

```
[ ] Crear backend/routers/complemento.py:

        @router.put("/{agendamiento_id}",
                    response_model=ComplementoOutput)
        def upsert_complemento(
            agendamiento_id: int,
            payload: ComplementoInput,
            db: Session = Depends(get_db),
            current_user: dict = Depends(get_current_user)
        ):
            # 1. Solo doctores pueden escribir
            if current_user["rol"] != "doctor":
                raise HTTPException(status_code=403,
                    detail="Solo médicos pueden completar el parte diario")

            medico_id = current_user["medico_id"]

            # 2. Verificar que el agendamiento le pertenece al médico
            #    (seguridad: no se puede editar el parte de otro médico)
            pacientes = obtener_pacientes_his(medico_id, date.today())
            ids_propios = {p["AgendamientoId"] for p in pacientes}
            if agendamiento_id not in ids_propios:
                raise HTTPException(status_code=403,
                    detail="Este agendamiento no pertenece al médico autenticado")

            # 3. UPSERT
            existente = db.query(ComplementoParteDiario).filter_by(
                AgendamientoId=agendamiento_id).first()

            if existente:
                for campo, valor in payload.model_dump().items():
                    setattr(existente, campo, valor)
                registro = existente
            else:
                registro = ComplementoParteDiario(
                    AgendamientoId = agendamiento_id,
                    MedicoId       = medico_id,
                    FechaParte     = date.today(),
                    CreadoPor      = current_user["id"],
                    **payload.model_dump()
                )
                db.add(registro)

            db.commit()
            db.refresh(registro)
            return registro

[ ] Registrar el router en main.py con prefix="/complemento"
```

✎ **Criterio de aceptación:**
- `PUT /complemento/1001` con token del doctor dueño → HTTP 200, registro guardado.
- `PUT /complemento/1004` con token de `dr.gutierrez` (MedicoId=10, pero 1004 pertenece a MedicoId=11) → HTTP 403.
- Llamar al mismo endpoint dos veces con datos distintos → el segundo actualiza, no duplica.

---

## Día 9 — Merge service y endpoint unificado

### Tarea 9.1 — Implementar `merge_service.py`

```
[ ] Crear backend/services/merge_service.py con la función
    obtener_parte_diario_completo(db, medico_id, fecha)
    definida íntegramente en la Sección 5.2 del documento
    02_Arquitectura_y_Base_Datos.md

[ ] La función debe:
    - Consultar el HIS (his_service)
    - Consultar la BD local con un IN de AgendamientoIds
    - Construir el dict de lookup O(1)
    - Retornar lista[RegistroParteDiario] con Complemento
      adjunto si existe, o null si aún no se llenó
```

### Tarea 9.2 — Actualizar `GET /agenda/dia` para usar el merge

```
[ ] Modificar backend/routers/agenda.py para que llame a
    merge_service.obtener_parte_diario_completo()
    en lugar de his_service directamente

[ ] Agregar endpoint para el enfermero:

        @router.get("/global", response_model=list[RegistroParteDiario])
        def get_agenda_global(
            fecha_inicio: date = Query(default=date.today()),
            fecha_fin:    date = Query(default=date.today()),
            medico_id:    Optional[int] = Query(default=None),
            current_user: dict = Depends(get_current_user)
        ):
            if current_user["rol"] != "enfermero":
                raise HTTPException(status_code=403)
            # Por ahora retorna todos los registros del mock
            # filtrados por medico_id si se provee
            ...
```

---

## Día 10 — Pruebas integradas de Fase 2

### Tarea 10.1 — Checklist de pruebas de escritura

```
[ ] Flujo completo del médico:
    [ ] Login como dr.gutierrez → obtener JWT
    [ ] GET /agenda/dia → 3 pacientes, todos con Complemento=null
    [ ] PUT /complemento/1001 con datos válidos → 200
    [ ] PUT /complemento/1001 con datos distintos → 200 (actualiza)
    [ ] GET /agenda/dia nuevamente → AgendamientoId=1001
        ahora tiene Complemento con datos y ComplementoCompleto=true
    [ ] PUT /complemento/1004 → 403 (no es su paciente)
    [ ] PUT /complemento/1002 con TipoConsulta="INVALIDO" → 422

[ ] Flujo validación de campos:
    [ ] PUT sin EspecialidadId → 422 Unprocessable Entity
    [ ] PUT sin TipoConsulta → 422
    [ ] PUT con todos los checkboxes en false → 200 (válido)
    [ ] PUT con todos los checkboxes en true → 200 (válido)
```

### Tarea 10.2 — Cierre de Fase 2

```
[ ] Commit: "feat: fase-2 - BD local SQLite + endpoints UPSERT"
[ ] Pull Request de feature/fase-2 → develop
[ ] Verificar que alembic upgrade head funciona en BD limpia
[ ] Documentar el comando de semilla en el README
```

⚠ **Bloqueante para Fase 3:** el flujo GET → PUT → GET con datos persistidos debe funcionar de extremo a extremo antes de iniciar el frontend.

---

---

# FASE 3 — Frontend: Vistas Doctor y Enfermero

**Objetivo:** Desarrollar la interfaz de usuario con los colores corporativos de SOLCA, integrando la vista de agenda del médico (con edición en línea y selectores dinámicos) y la vista global del enfermero.

**Duración:** 7–10 días hábiles  
**Rama Git:** `feature/fase-3-frontend`  
**Stack recomendado:** React 18 + Vite · Tailwind CSS (o CSS puro con variables SOLCA)

---

## Día 11 — Configuración del proyecto frontend

### Tarea 11.1 — Inicializar proyecto React

```
[ ] Desde la raíz del repositorio:
        npm create vite@latest frontend -- --template react
        cd frontend
        npm install

[ ] Instalar dependencias de UI y utilidades:
        npm install axios react-router-dom
        npm install -D tailwindcss postcss autoprefixer
        npx tailwindcss init -p
```

### Tarea 11.2 — Configurar variables de colores SOLCA

```
[ ] Crear frontend/src/styles/variables.css:

        :root {
          --color-primario:     #003366;   /* Azul oscuro SOLCA */
          --color-primario-hover: #004080;
          --color-fondo:        #FFFFFF;   /* Blanco */
          --color-texto:        #2C2C2C;
          --color-fila-alterna: #F5F7FA;
          --color-completo:     #27AE60;   /* Verde — fila completa */
          --color-borde:        #D0D7DE;
          --color-error:        #C0392B;
          --color-guardado:     #2ECC71;   /* Indicador auto-save */
        }

[ ] Extender tailwind.config.js con los tokens:

        colors: {
          'solca-azul':    '#003366',
          'solca-blanco':  '#FFFFFF',
          'solca-fila':    '#F5F7FA',
          'solca-verde':   '#27AE60',
          'solca-borde':   '#D0D7DE',
        }
```

### Tarea 11.3 — Configurar React Router y contexto de autenticación

```
[ ] Crear frontend/src/context/AuthContext.jsx:
    - Estado: { token, usuario, rol, medicoId }
    - Funciones: login(username, password), logout()
    - login() llama a POST /auth/login y guarda el JWT
      en memoria (variable de estado, NO en localStorage)
    - Proveer el contexto en main.jsx

[ ] Crear frontend/src/router/AppRouter.jsx:
    - Ruta "/" → LoginPage
    - Ruta "/doctor" → AgendaPage (protegida, rol=doctor)
    - Ruta "/enfermero" → GlobalPage (protegida, rol=enfermero)
    - Componente PrivateRoute que verifica el token del contexto
    - Redirigir a "/" si no hay token
```

---

## Día 12 — Página de Login

### Tarea 12.1 — Componente LoginPage

```
[ ] Crear frontend/src/pages/LoginPage.jsx:

    Diseño:
    - Fondo blanco (#FFFFFF)
    - Logo institucional de SOLCA centrado en la parte superior
    - Formulario centrado verticalmente en la pantalla
    - Título: "Sistema de Parte Diario Médico"
      (fuente: Arial o similar, color: #003366, tamaño: 24px)
    - Campo: "Usuario"  (input type=text)
    - Campo: "Contraseña"  (input type=password)
    - Botón "Ingresar":
        · Fondo: #003366  ·  Texto: blanco
        · Hover: #004080
        · Ancho: 100% del formulario
    - Mensaje de error discreto bajo el botón (texto rojo #C0392B)
      si las credenciales son inválidas
    - Sin imágenes decorativas ni animaciones que distraigan

    Comportamiento:
    [ ] Al enviar, llamar a AuthContext.login()
    [ ] Si login exitoso → redirigir según rol:
          rol=doctor   → /doctor
          rol=enfermero → /enfermero
    [ ] Si login falla → mostrar mensaje de error bajo el botón
    [ ] El botón debe mostrar "Ingresando..." durante la llamada a la API
    [ ] Deshabilitar el botón durante la llamada (evitar doble submit)
```

✎ **Criterio de aceptación:** el login con credenciales de prueba redirige a la vista correcta. Con credenciales incorrectas muestra el error sin romper la página.

---

## Día 13 — Vista del Doctor: tabla de agenda

### Tarea 13.1 — Layout base del Doctor

```
[ ] Crear frontend/src/layouts/DoctorLayout.jsx:

    - Barra superior (navbar):
        · Fondo: #003366  ·  Texto: blanco
        · Izquierda: logo SOLCA + texto "Parte Diario Médico"
        · Derecha: nombre del doctor (del AuthContext) + botón "Cerrar sesión"
    - Contenido principal: fondo blanco, padding 24px
    - Sin sidebar (no se necesita navegación adicional en el rol doctor)
```

### Tarea 13.2 — Componente de tabla de agenda

```
[ ] Crear frontend/src/pages/AgendaPage.jsx:

    Al montar el componente:
    [ ] Llamar a GET /agenda/dia con el JWT del contexto
    [ ] Mostrar spinner de carga mientras la API responde
    [ ] Si la lista está vacía → mostrar mensaje "No hay pacientes
        agendados para hoy"

    Columnas de la tabla (en orden):
    | # | N° HC | Apellidos | Nombres | Edad | Sexo |
    | CIE10 | Diagnóstico | Convenio | Especialidad |
    | Actividad | Tipo Consulta | PRE QT | PRE QX | QUIMIO | EKG |

    Diseño de la tabla:
    [ ] Encabezado: fondo #003366, texto blanco, bold
    [ ] Filas alternas: blanco / #F5F7FA
    [ ] Fila con ComplementoCompleto=true: indicador verde
        (punto verde • o ícono ✓ en la primera columna)
    [ ] Texto de celdas: #2C2C2C, 14px mínimo
    [ ] Bordes: 1px solid #D0D7DE
    [ ] Sin scroll horizontal en resoluciones >= 1280px
        (ajustar anchos de columna para que quepan)
```

---

## Día 14 — Edición en línea y selectores dinámicos

### Tarea 14.1 — Campos editables en la tabla (edición en línea)

```
[ ] Las columnas editables deben activarse al hacer clic
    en la celda correspondiente (sin abrir modales):

    Especialidad:
    [ ] Mostrar <select> con las opciones de GET /catalogos/especialidades
    [ ] Cargar las opciones UNA sola vez al montar la página
        (guardar en estado, no re-consultar por cada fila)

    Actividad:
    [ ] Mostrar <select> deshabilitado hasta que haya especialidad seleccionada
    [ ] Al cambiar la Especialidad:
        · Limpiar el valor de Actividad
        · Habilitar el selector
        · Filtrar las actividades del estado local por EspecialidadId
          (NO llamar a la API nuevamente — los datos ya están en memoria)

    Tipo de Consulta:
    [ ] Mostrar <select> con dos opciones:
        "Primera Vez" (valor: PRIMERA_VEZ)
        "Subsecuente" (valor: SUBSECUENTE)

    Checkboxes PRE QT · PRE QX · QUIMIO · EKG:
    [ ] Checkboxes grandes (20×20px mínimo) con su etiqueta
    [ ] Marcar/desmarcar directamente en la celda, sin clic extra
```

### Tarea 14.2 — Auto-guardado con debounce

```
[ ] Crear frontend/src/hooks/useAutoGuardado.js:

        import { useCallback, useRef } from "react";
        import { apiClient } from "../services/api";

        export function useAutoGuardado(agendamientoId) {
          const timerRef = useRef(null);

          const guardar = useCallback((datos) => {
            clearTimeout(timerRef.current);
            timerRef.current = setTimeout(async () => {
              try {
                await apiClient.put(
                  `/complemento/${agendamientoId}`,
                  datos
                );
                // Mostrar indicador "✓ Guardado" por 2 segundos
                // usando estado local del componente padre
              } catch (err) {
                // Mostrar indicador de error sin bloquear
                console.error("Error al guardar:", err);
              }
            }, 500); // 500ms de debounce
          }, [agendamientoId]);

          return guardar;
        }

[ ] El indicador de guardado debe aparecer en la misma fila
    de la tabla (esquina derecha de la fila), no en un toast
    global ni en un modal

[ ] El indicador desaparece automáticamente a los 2 segundos
[ ] Nunca bloquear la tabla mientras se guarda
```

✎ **Criterio de aceptación:** al cambiar cualquier campo editable, la llamada a `PUT /complemento/{id}` se realiza en segundo plano. El usuario puede seguir editando otra fila sin esperar. El indicador "✓ Guardado" aparece y desaparece sin interrupciones.

---

## Día 15 — Vista del Enfermero

### Tarea 15.1 — Layout y página de vista global

```
[ ] Crear frontend/src/pages/GlobalPage.jsx:

    Barra de filtros (parte superior, fondo #F5F7FA con borde inferior):
    [ ] Selector de fecha inicio  (input type=date)
    [ ] Selector de fecha fin     (input type=date)
    [ ] Selector de médico        (<select> con opción "Todos los médicos")
    [ ] Botón "Aplicar filtros"   (estilo primario SOLCA: #003366)
    [ ] Botón "Concentrado Mensual" (estilo secundario: borde azul, fondo blanco)

    Tabla de vista global:
    [ ] Mismas columnas que la vista del doctor
    [ ] Agregar columna "Médico" al inicio
    [ ] Todos los campos en modo solo lectura (sin elementos editables)
    [ ] Filas con ComplementoCompleto=false resaltadas sutilmente
        (sin color llamativo, solo texto gris más claro)
    [ ] Paginación si hay más de 50 registros en pantalla

    Panel de sumario (debajo de los filtros, antes de la tabla):
    [ ] Contador de total de pacientes en la vista actual
    [ ] Contador de partes completos vs. pendientes
```

### Tarea 15.2 — Botones de exportación

```
[ ] En la vista del doctor (AgendaPage):
    [ ] Dos botones fijos en la parte superior derecha:
        "⬇ PDF"  y  "⬇ Excel"
    [ ] Al hacer clic, llamar al endpoint correspondiente
        y descargar el archivo directamente:

            const response = await apiClient.get(
              "/exportar/pdf?fecha=2026-06-27",
              { responseType: "blob" }
            );
            const url = URL.createObjectURL(response.data);
            const a = document.createElement("a");
            a.href = url;
            a.download = `ParteDiario_Dr_${fecha}.pdf`;
            a.click();

[ ] En la vista del enfermero (GlobalPage):
    [ ] Botón "⬇ Concentrado Excel" visible junto a los filtros
    [ ] Al hacer clic, descargar el archivo con los filtros activos
```

---

## Día 16 — Refinamiento visual y pruebas de UI

### Tarea 16.1 — Revisión de consistencia visual

```
[ ] Verificar en todas las vistas:
    [ ] Color de fondo: siempre blanco
    [ ] Navbar: siempre azul oscuro #003366
    [ ] Botones primarios: #003366 con texto blanco
    [ ] No hay grises medios ni colores que no sean de la paleta SOLCA
    [ ] Tipografía consistente: Arial o similar sans-serif
    [ ] Espaciado suficiente entre filas (padding-y mínimo 12px)
    [ ] Sin scroll horizontal en 1280px de ancho

[ ] Verificar ausencia de modales innecesarios:
    [ ] El cambio de especialidad no abre confirmación
    [ ] El auto-guardado no abre confirmación
    [ ] La exportación descarga directamente (sin "¿está seguro?")
    [ ] El único modal permitido es en logout (opcional)

[ ] Probar en resoluciones: 1280×720, 1440×900, 1920×1080
```

### Tarea 16.2 — Pruebas funcionales del frontend

```
[ ] Login y redirección por rol
[ ] La tabla del doctor solo muestra sus pacientes
[ ] Cambiar Especialidad limpia y recarga Actividad correctamente
[ ] Marcar checkbox Pre_QT y verificar que se guardó
    (recargar la página y confirmar que el check persiste)
[ ] La vista del enfermero muestra todos los médicos
[ ] El filtro por médico reduce la tabla correctamente
[ ] Los botones PDF/Excel disparan la descarga
```

### Tarea 16.3 — Cierre de Fase 3

```
[ ] Commit: "feat: fase-3 - frontend vistas doctor y enfermero"
[ ] Pull Request de feature/fase-3 → develop
[ ] Demo interna con el equipo médico de SOLCA para
    validar flujo y detectar ajustes antes de la Fase 4
[ ] Registrar feedback del equipo médico en el issue tracker
```

---

---

# FASE 4 — Reportes Exportables y Conexión SQL Server

**Objetivo:** Implementar la generación de PDF y Excel, el Concentrado Mensual con sumatorias, y migrar la fuente de datos del mock JSON a la vista SQL real de RELIV.

**Duración:** 5 días hábiles  
**Rama Git:** `feature/fase-4-reportes-sql`

---

## Día 17 — Generación de PDF del Parte Diario

### Tarea 17.1 — Instalar librerías de reportes

```
[ ] Agregar a requirements.txt:
        reportlab==4.2.0       # Generación PDF
        openpyxl==3.1.2        # Generación Excel .xlsx

[ ] Instalar:
        pip install -r requirements.txt
```

### Tarea 17.2 — Implementar generación de PDF

```
[ ] Crear backend/services/export_service.py

[ ] Función generar_pdf_parte_diario(registros, medico_nombre, fecha):

    Estructura del PDF:
    [ ] Encabezado institucional:
        · Logo SOLCA (imagen PNG provista por la institución)
        · Texto: "SOCIEDAD DE LUCHA CONTRA EL CÁNCER — SOLCA"
        · Texto: "Parte Diario Médico"
        · Médico: [nombre completo]  ·  Fecha: [DD/MM/YYYY]
        · Línea separadora de color #003366

    [ ] Tabla de pacientes:
        · Columnas: N°HC · Apellidos/Nombres · Edad · Sexo ·
          Diagnóstico · CIE10 · Convenio · Especialidad ·
          Actividad · Tipo Consulta · QT · QX · Quimio · EKG
        · Encabezado de tabla: fondo #003366, texto blanco
        · Filas alternas: blanco / #F5F7FA
        · Fuente: Helvetica 8pt para contenido, 9pt bold para encabezado

    [ ] Pie de página:
        · "Documento generado el [fecha y hora] por el Sistema de
          Parte Diario Médico — SOLCA"
        · Número de página: Página X de Y

    [ ] Orientación: horizontal (landscape) para caber todas las columnas

[ ] Crear endpoint:

        @router.get("/pdf")
        def exportar_pdf(
            fecha: date = Query(default=date.today()),
            db: Session = Depends(get_db),
            current_user: dict = Depends(get_current_user)
        ):
            medico_id = current_user["medico_id"]
            registros = obtener_parte_diario_completo(db, medico_id, fecha)
            pdf_bytes = generar_pdf_parte_diario(
                registros,
                medico_nombre=current_user["nombre_completo"],
                fecha=fecha
            )
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition":
                    f'attachment; filename="ParteDiario_{fecha}.pdf"'
                }
            )
```

✎ **Criterio de aceptación:** el PDF descargado abre correctamente en un visor PDF, muestra el encabezado SOLCA y contiene todos los pacientes del médico del día solicitado con sus complementos.

---

## Día 18 — Generación de Excel del Parte Diario y Concentrado Mensual

### Tarea 18.1 — Excel del Parte Diario individual

```
[ ] Función generar_excel_parte_diario(registros, medico_nombre, fecha):
    Usando openpyxl:

    [ ] Hoja: "Parte Diario"
    [ ] Fila 1: título "SOLCA — Parte Diario Médico"
        (fuente 14pt bold, color #003366, merge de celdas A1:N1)
    [ ] Fila 2: "Médico: [nombre]  |  Fecha: [fecha]"
    [ ] Fila 3: vacía (separador)
    [ ] Fila 4: encabezados de columnas
        (fondo #003366, fuente blanca, bold, bordes)
    [ ] Filas 5+: datos de pacientes
        (filas alternas con relleno #F5F7FA)
    [ ] Checkboxes exportados como "SÍ" / "" (vacío)
    [ ] Ajustar ancho de columnas automáticamente (auto-fit)
    [ ] Fila de totales al pie:
        · Total de filas
        · Suma de cada checkbox (SÍ = 1)

[ ] Crear endpoint GET /exportar/excel
    (misma lógica de seguridad que el PDF)
```

### Tarea 18.2 — Concentrado Mensual en Excel

```
[ ] Función generar_concentrado_mensual(db, medico_ids, fecha_inicio, fecha_fin):

    [ ] Consultar BD local Complemento_Parte_Diario filtrando por:
        · FechaParte BETWEEN fecha_inicio AND fecha_fin
        · MedicoId IN medico_ids (o todos si la lista está vacía)

    [ ] Hacer merge con HIS para obtener datos del paciente
        (N_HC, Apellidos, Nombres, Diagnóstico, CIE10, Convenio)

    [ ] Hoja 1 — "Detalle":
        · Una fila por paciente atendido en el período
        · Columnas: Fecha · Médico · Especialidad · Actividad ·
          N°HC · Apellidos · Nombres · Edad · Sexo ·
          Diagnóstico · Convenio · Tipo Consulta ·
          PRE QT · PRE QX · QUIMIO · EKG

    [ ] Hoja 2 — "Resumen por Médico":
        Columnas: Médico · Total Pacientes · Primera Vez ·
                  Subsecuente · PRE QT · PRE QX · QUIMIO · EKG
        Una fila por médico + fila de TOTALES GENERALES al pie
        (fondo #003366, texto blanco, bold)

    [ ] Hoja 3 — "Resumen por Especialidad":
        Columnas: Especialidad · Total · Primera Vez · Subsecuente ·
                  PRE QT · PRE QX · QUIMIO · EKG
        Una fila por especialidad + fila de TOTALES al pie

[ ] Crear endpoint:

        GET /concentrado/mensual/exportar
            ?fecha_inicio=YYYY-MM-DD
            &fecha_fin=YYYY-MM-DD
            &medico_ids=10,11,12   (opcional; vacío = todos)

        Solo accesible para rol=enfermero
        Retorna StreamingResponse con el .xlsx
```

✎ **Criterio de aceptación:** el Excel descargado tiene 3 hojas. La hoja "Resumen por Médico" muestra totales correctos verificables contra el detalle de la Hoja 1.

---

## Día 19 — Migración de mock a SQL Server (RELIV)

### Tarea 19.1 — Instalar driver de SQL Server

```
[ ] Agregar a requirements.txt:
        pyodbc==5.1.0
        # O alternativamente: pymssql==2.3.0

[ ] Instalar:
        pip install -r requirements.txt

[ ] Verificar driver ODBC disponible en el servidor:
        python -c "import pyodbc; print(pyodbc.drivers())"
        # Debe aparecer "ODBC Driver 17 for SQL Server" o superior
        # Si no aparece, instalar el driver de Microsoft
```

### Tarea 19.2 — Configurar segundo engine para el HIS

```
[ ] Agregar a backend/database.py:

        from sqlalchemy import create_engine as ce
        from backend.config import settings
        import urllib

        def _his_engine():
            params = urllib.parse.quote_plus(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={settings.HIS_DB_SERVER};"
                f"DATABASE={settings.HIS_DB_NAME};"
                f"UID={settings.HIS_DB_USER};"
                f"PWD={settings.HIS_DB_PASSWORD};"
                "TrustServerCertificate=yes;"
            )
            return ce(f"mssql+pyodbc:///?odbc_connect={params}",
                      pool_pre_ping=True, pool_size=3, max_overflow=5)

        his_engine = _his_engine() if settings.HIS_DATA_SOURCE == "sql" else None
```

### Tarea 19.3 — Actualizar `his_service.py` para modo SQL

```
[ ] Modificar backend/services/his_service.py:

        def obtener_pacientes_his(medico_id, fecha):
            if settings.HIS_DATA_SOURCE == "mock":
                return _obtener_desde_mock(medico_id)
            else:
                return _obtener_desde_sql(medico_id, fecha)

        def _obtener_desde_sql(medico_id, fecha):
            from backend.database import his_engine
            from sqlalchemy import text

            QUERY = text("""
                SELECT
                    AG.Id           AS AgendamientoId,
                    AG.MedicoId     AS MedicoId,
                    PC.IDENTIFICACION AS N_HC,
                    CONCAT(PC.PRIMERAPELLIDO, ' ',
                           PC.SEGUNDOAPELLIDO) AS APELLIDOS,
                    PC.NOMBRE       AS NOMBRES,
                    CAST(PC.FechaNacimiento AS DATE) AS FECHA_NACIMIENTO,
                    FLOOR(DATEDIFF(DAY, PC.FechaNacimiento,
                          GETDATE()) / 365.25) AS EDAD,
                    CS.DESCRIPCION  AS SEXO,
                    DP.CIE10_Codes  AS CIE10,
                    DP.Diagnostico_Desc AS DIAGNOSTICO,
                    PC.DIRECCION    AS PROCEDENCIA,
                    TC_CONV.Nombre  AS CONVENIO
                FROM [dbo].[AgendamientoSolcaT] AG
                INNER JOIN [dbo].[PacientesSolcaT] PC
                    ON AG.PacienteId = PC.ID
                INNER JOIN [dbo].[AdmisionesSolcaT] AD
                    ON AG.Id = AD.AgendandamientoId
                INNER JOIN [dbo].[EnfermedadActualSolcaT] EA
                    ON AD.Codigo = EA.CódigoAdmisión
                LEFT JOIN [dbo].[TipoCategoria] CS
                    ON PC.SEXOID = CS.Id
                LEFT JOIN [dbo].[AdmisionesSeguroSolcaT] ADS
                    ON AD.Id = ADS.AdmissionId
                LEFT JOIN [dbo].[ConveniosSolcaT] TC_CONV
                    ON ADS.ConvenioId = TC_CONV.Id
                OUTER APPLY (
                    SELECT
                        STRING_AGG(C.Codigo, ' ; ')      AS CIE10_Codes,
                        STRING_AGG(C.Descripcion, ' ; ') AS Diagnostico_Desc
                    FROM (
                        SELECT LTRIM(RTRIM(REPLACE(REPLACE(
                               value, CHAR(13), ''), CHAR(10), '')))
                               AS CleanValue
                        FROM STRING_SPLIT(EA.DiagnósticosCIE10, ';')
                    ) AS S
                    CROSS APPLY (
                        SELECT
                            CASE WHEN CHARINDEX(' - ', S.CleanValue) > 0
                            THEN LTRIM(RTRIM(LEFT(S.CleanValue,
                                 CHARINDEX(' - ', S.CleanValue) - 1)))
                            ELSE S.CleanValue END AS CodigoExtraido
                    ) AS Ext
                    LEFT JOIN [dbo].[Cie10] C
                        ON Ext.CodigoExtraido = C.Codigo
                    WHERE S.CleanValue <> ''
                ) AS DP
                WHERE EA.DiagnósticosCIE10 IS NOT NULL
                  AND CAST(AG.Fecha AS DATE) = :fecha
                  AND AG.MedicoId            = :medico_id
                ORDER BY AG.Fecha ASC
            """)

            with his_engine.connect() as conn:
                rows = conn.execute(QUERY,
                    {"fecha": fecha, "medico_id": medico_id})
                return [dict(r._mapping) for r in rows]

[ ] Verificar que la query es idéntica a la proporcionada
    en el documento de requisitos (solo se añade el filtro
    AND AG.MedicoId = :medico_id)

[ ] Confirmar con el equipo RELIV el nombre exacto del campo
    MedicoId en AgendamientoSolcaT (puede llamarse DoctorId,
    MedicoAsignado u otro nombre — VERIFICAR antes de ejecutar)
```

### Tarea 19.4 — Prueba de conexión al HIS

```
[ ] Script de prueba rápida (ejecutar solo en red SOLCA):

        python - <<'EOF'
        from backend.services.his_service import obtener_pacientes_his
        from backend.config import settings
        import datetime

        # Cambiar temporalmente a modo sql
        settings.HIS_DATA_SOURCE = "sql"

        pacientes = obtener_pacientes_his(
            medico_id=<ID_REAL_DE_UN_MEDICO>,
            fecha=datetime.date.today()
        )
        print(f"Pacientes encontrados: {len(pacientes)}")
        if pacientes:
            print("Primer paciente:", pacientes[0])
        EOF

[ ] Si la conexión falla, verificar:
    [ ] Firewall entre el servidor de la app y SQL Server de RELIV
    [ ] Credenciales en el .env de producción
    [ ] Driver ODBC instalado correctamente
    [ ] El campo MedicoId existe en AgendamientoSolcaT
```

---

## Día 20 — Pruebas finales e integración completa

### Tarea 20.1 — Pruebas end-to-end del sistema completo

```
[ ] Con HIS_DATA_SOURCE=mock (siempre funciona sin red):
    [ ] Login doctor → ver agenda → completar todos los campos
        de 3 pacientes → exportar PDF → verificar contenido PDF
    [ ] Login doctor → exportar Excel → verificar 3 hojas no aplica
        (parte individual solo tiene 1 hoja) → verificar totales al pie
    [ ] Login enfermero → vista global → filtrar por médico 10
        → solo aparecen pacientes de MedicoId=10
    [ ] Login enfermero → filtrar por rango del mes → exportar
        Concentrado Mensual → verificar 3 hojas del Excel

[ ] Con HIS_DATA_SOURCE=sql (solo si hay conexión a RELIV):
    [ ] Repetir el flujo completo del doctor con datos reales
    [ ] Verificar que los campos N_HC, APELLIDOS, DIAGNOSTICO, CIE10
        llegan correctamente desde SQL Server
    [ ] Verificar que el filtro por MedicoId funciona con el ID real

[ ] Pruebas de seguridad:
    [ ] Un doctor no puede ver /agenda/global → 403
    [ ] Un enfermero no puede hacer PUT /complemento → 403
    [ ] Token expirado → 401 en cualquier endpoint protegido
    [ ] Modificar manualmente el medico_id en el JWT → el backend
        rechaza (verificar firma del token)
```

### Tarea 20.2 — Cambiar a modo producción (PostgreSQL)

```
[ ] Si se decide migrar de SQLite a PostgreSQL antes del deploy:
    [ ] Crear base de datos en el servidor PostgreSQL de SOLCA:
            CREATE DATABASE solca_parte_diario;
    [ ] Actualizar DATABASE_URL en .env de producción:
            DATABASE_URL=postgresql://user:pass@host:5432/solca_parte_diario
    [ ] Ejecutar migraciones en la BD de producción:
            alembic upgrade head
    [ ] Ejecutar semilla de catálogos:
            python -m backend.seed
    [ ] Quitar connect_args de database.py (solo era para SQLite)
```

### Tarea 20.3 — Cierre de Fase 4 y entrega final

```
[ ] Commit: "feat: fase-4 - reportes PDF/Excel + conexion SQL Server"
[ ] Pull Request de feature/fase-4 → develop
[ ] Merge de develop → main con tag de versión: v1.0.0
[ ] Generar documentación de despliegue (README de producción):
    [ ] Requisitos del servidor (Python 3.11+, ODBC Driver 17)
    [ ] Variables de entorno requeridas
    [ ] Comandos de arranque del backend
    [ ] Comandos de arranque del frontend (build + serve)
    [ ] Comando de migración y semilla inicial
[ ] Sesión de capacitación con el personal de SOLCA:
    [ ] Demo con médicos (flujo del parte diario)
    [ ] Demo con enfermería (filtros y concentrado mensual)
    [ ] Entrega de manual de usuario (documento separado)
```

---

## Resumen de Entregables por Fase

| Fase | Archivos creados / modificados | Verificable en |
|---|---|---|
| 1 | `main.py` · `config.py` · `auth.py` · `agenda.py` · `catalogos.py` · `his_service.py` · `mock_data.json` | `GET /agenda/dia` filtra por médico · Swagger UI |
| 2 | `database.py` · `complemento.py (model)` · `complemento.py (router)` · `merge_service.py` · `seed.py` · migración Alembic | Persistencia tras reload · UPSERT verificado |
| 3 | `LoginPage.jsx` · `AgendaPage.jsx` · `GlobalPage.jsx` · `AuthContext.jsx` · `useAutoGuardado.js` · `variables.css` | Demo visual en navegador · colores SOLCA · sin modales |
| 4 | `export_service.py` · `exportacion.py (router)` · `concentrado.py (router)` · `his_service.py (modo SQL)` | PDF descargable · Excel 3 hojas · datos reales RELIV |

---

*Documento elaborado por el equipo de Project Management. Actualizar el estado de cada tarea (`[ ]` → `[x]`) durante la ejecución del sprint correspondiente.*
