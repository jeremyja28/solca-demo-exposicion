# 02 — Arquitectura y Base de Datos
## Sistema de Parte Diario Médico — SOLCA

> **Versión:** 1.0  
> **Fecha:** Junio 2026  
> **Estado:** Borrador para revisión  
> **Dependencia:** Documento `01_Requisitos_y_Casos_Uso.md`

---

## 1. Visión General de la Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Browser)                        │
│              React / HTML+JS  ·  Colores SOLCA                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │  HTTP / JSON (REST)
┌──────────────────────────▼──────────────────────────────────────┐
│                     BACKEND (Python)                            │
│              FastAPI  ·  Puerto 8000                            │
│                                                                 │
│   ┌─────────────────┐        ┌──────────────────────────────┐   │
│   │  Capa de Datos  │        │       Capa de Negocio        │   │
│   │                 │        │                              │   │
│   │  ① Fuente HIS   │──────►│  merge_parte_diario()        │   │
│   │  mock_data.json │  JOIN  │  Combina HIS + Complemento  │   │
│   │  (→ SQL real)   │◄──────│  en memoria antes de         │   │
│   │                 │        │  responder al cliente        │   │
│   │  ② BD Local     │        │                              │   │
│   │  SQLite / PG    │        └──────────────────────────────┘   │
│   │  Complemento_   │                                           │
│   │  Parte_Diario   │                                           │
│   └─────────────────┘                                           │
└─────────────────────────────────────────────────────────────────┘
```

### 1.1 Stack tecnológico

| Capa | Tecnología | Justificación |
|---|---|---|
| Backend | **FastAPI** (Python 3.11+) | Validación automática con Pydantic, OpenAPI nativa, async listo para conectar al HIS real |
| ORM | **SQLAlchemy 2.x** | Abstracción de BD; permite migrar de SQLite a PostgreSQL sin cambiar el código de negocio |
| BD local (desarrollo) | **SQLite** | Sin instalación, archivo único, ideal para fase de prototipo |
| BD local (producción) | **PostgreSQL 15+** | Robustez, concurrencia, respaldos SOLCA |
| Fuente HIS (temporal) | **mock_data.json** | Simula la vista SQL de RELIV mientras se gestiona acceso a la BD hospitalaria |
| Fuente HIS (producción) | **pyodbc / SQLAlchemy + SQL Server** | Conexión directa a las vistas de `AgendamientoSolcaT` y relacionadas |
| Autenticación | **JWT (python-jose)** | Tokens con claim de `rol` y `medico_id` para filtrado seguro en backend |
| Migraciones | **Alembic** | Control de versiones del esquema de la BD local |

---

## 2. Estructura del Proyecto

```
solca-parte-diario/
│
├── backend/
│   ├── main.py                  # Entrada FastAPI, registro de routers
│   ├── config.py                # Variables de entorno (DATABASE_URL, SECRET_KEY, etc.)
│   ├── database.py              # Engine SQLAlchemy, SessionLocal, Base declarativa
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── complemento.py       # Modelo ORM: Complemento_Parte_Diario
│   │   ├── especialidad.py      # Modelo ORM: Especialidad
│   │   └── actividad.py         # Modelo ORM: Actividad
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── complemento.py       # Pydantic: entrada y salida de la API
│   │   └── parte_diario.py      # Pydantic: schema del registro unificado (HIS + Complemento)
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py              # POST /auth/login
│   │   ├── agenda.py            # GET /agenda/dia  (vista del médico)
│   │   ├── complemento.py       # PUT /complemento/{agendamiento_id}
│   │   ├── exportacion.py       # GET /exportar/pdf  GET /exportar/excel
│   │   └── concentrado.py       # GET /concentrado/mensual  (vista enfermero)
│   │
│   ├── services/
│   │   ├── his_service.py       # Carga mock_data.json (→ SQL real en producción)
│   │   ├── merge_service.py     # Lógica del JOIN en memoria (HIS + BD local)
│   │   └── export_service.py    # Generación PDF y Excel
│   │
│   ├── data/
│   │   └── mock_data.json       # ← Datos de prueba (ver Sección 4)
│   │
│   ├── migrations/              # Alembic
│   │   └── versions/
│   │
│   └── requirements.txt
│
└── frontend/                    # (scope del documento 03)
```

---

## 3. Base de Datos Local

### 3.1 Tabla principal: `Complemento_Parte_Diario`

Esta tabla almacena **únicamente** los campos que el médico completa manualmente. Todo lo demás viene del HIS y no se duplica en la BD local.

```sql
CREATE TABLE Complemento_Parte_Diario (
    Id                  INTEGER     PRIMARY KEY AUTOINCREMENT,  -- SERIAL en PostgreSQL

    -- Llave de enlace con la vista HIS (AgendamientoSolcaT.Id)
    AgendamientoId      INTEGER     NOT NULL UNIQUE,

    -- Llave del médico que registró (para auditoría y filtrado)
    MedicoId            INTEGER     NOT NULL,

    -- Fecha del parte (denormalizada intencionalmente para
    -- facilitar queries del Concentrado Mensual sin volver al HIS)
    FechaParte          DATE        NOT NULL,

    -- Campos complementarios que llena el médico
    EspecialidadId      INTEGER     NOT NULL REFERENCES Especialidad(Id),
    ActividadId         INTEGER     NOT NULL REFERENCES Actividad(Id),
    TipoConsulta        VARCHAR(15) NOT NULL
                            CHECK (TipoConsulta IN ('PRIMERA_VEZ', 'SUBSECUENTE')),
    Pre_QT              BOOLEAN     NOT NULL DEFAULT FALSE,
    Pre_QX              BOOLEAN     NOT NULL DEFAULT FALSE,
    Quimio              BOOLEAN     NOT NULL DEFAULT FALSE,
    EKG                 BOOLEAN     NOT NULL DEFAULT FALSE,

    -- Auditoría
    CreadoEn            DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ActualizadoEn       DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CreadoPor           INTEGER     NOT NULL   -- FK a tabla de usuarios del sistema
);

-- Índices para las consultas más frecuentes
CREATE INDEX idx_cpd_medico_fecha  ON Complemento_Parte_Diario (MedicoId, FechaParte);
CREATE INDEX idx_cpd_fecha         ON Complemento_Parte_Diario (FechaParte);
```

> **Decisión de diseño — `AgendamientoId UNIQUE`:** un agendamiento solo puede tener un complemento. Si el médico actualiza sus datos, se hace `UPDATE`, nunca `INSERT` duplicado. Esto evita inconsistencias en el Concentrado Mensual.

---

### 3.2 Tablas de catálogo: `Especialidad` y `Actividad`

```sql
CREATE TABLE Especialidad (
    Id          INTEGER     PRIMARY KEY AUTOINCREMENT,
    Nombre      VARCHAR(80) NOT NULL UNIQUE,
    Activa      BOOLEAN     NOT NULL DEFAULT TRUE
);

CREATE TABLE Actividad (
    Id              INTEGER     PRIMARY KEY AUTOINCREMENT,
    EspecialidadId  INTEGER     NOT NULL REFERENCES Especialidad(Id),
    Nombre          VARCHAR(100) NOT NULL,
    Activa          BOOLEAN     NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_actividad_especialidad ON Actividad (EspecialidadId);
```

**Datos iniciales (semilla):**

```sql
INSERT INTO Especialidad (Nombre) VALUES
    ('Oncología Médica'),
    ('Oncología Quirúrgica'),
    ('Radioterapia'),
    ('Hematología'),
    ('Cardiología'),
    ('Medicina Interna');

INSERT INTO Actividad (EspecialidadId, Nombre) VALUES
    (1, 'Consulta nueva'),
    (1, 'Consulta subsecuente'),
    (1, 'Valoración pre-QT'),
    (1, 'Valoración pre-QX'),
    (1, 'Control de QT'),
    (2, 'Consulta nueva'),
    (2, 'Consulta subsecuente'),
    (2, 'Valoración pre-QX'),
    (2, 'Seguimiento post-quirúrgico'),
    (3, 'Consulta nueva'),
    (3, 'Planificación de tratamiento'),
    (3, 'Seguimiento de tratamiento'),
    (4, 'Consulta nueva'),
    (4, 'Consulta subsecuente'),
    (4, 'Control de tratamiento'),
    (5, 'Consulta nueva'),
    (5, 'EKG'),
    (5, 'Valoración pre-QT'),
    (6, 'Consulta nueva'),
    (6, 'Consulta subsecuente'),
    (6, 'Interconsulta');
```

---

### 3.3 Modelo ORM (SQLAlchemy 2.x)

```python
# backend/models/complemento.py

from sqlalchemy import (
    Column, Integer, String, Boolean, Date,
    DateTime, ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class Especialidad(Base):
    __tablename__ = "Especialidad"

    Id     = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(80), nullable=False, unique=True)
    Activa = Column(Boolean, nullable=False, default=True)

    actividades = relationship("Actividad", back_populates="especialidad")


class Actividad(Base):
    __tablename__ = "Actividad"

    Id             = Column(Integer, primary_key=True, autoincrement=True)
    EspecialidadId = Column(Integer, ForeignKey("Especialidad.Id"), nullable=False)
    Nombre         = Column(String(100), nullable=False)
    Activa         = Column(Boolean, nullable=False, default=True)

    especialidad = relationship("Especialidad", back_populates="actividades")


class ComplementoParteDiario(Base):
    __tablename__ = "Complemento_Parte_Diario"

    __table_args__ = (
        CheckConstraint(
            "TipoConsulta IN ('PRIMERA_VEZ', 'SUBSECUENTE')",
            name="ck_tipo_consulta"
        ),
        UniqueConstraint("AgendamientoId", name="uq_agendamiento"),
    )

    Id             = Column(Integer, primary_key=True, autoincrement=True)
    AgendamientoId = Column(Integer, nullable=False)          # FK lógica → HIS
    MedicoId       = Column(Integer, nullable=False)
    FechaParte     = Column(Date,    nullable=False)
    EspecialidadId = Column(Integer, ForeignKey("Especialidad.Id"), nullable=False)
    ActividadId    = Column(Integer, ForeignKey("Actividad.Id"),    nullable=False)
    TipoConsulta   = Column(String(15), nullable=False)
    Pre_QT         = Column(Boolean, nullable=False, default=False)
    Pre_QX         = Column(Boolean, nullable=False, default=False)
    Quimio         = Column(Boolean, nullable=False, default=False)
    EKG            = Column(Boolean, nullable=False, default=False)
    CreadoEn       = Column(DateTime, server_default=func.now(), nullable=False)
    ActualizadoEn  = Column(DateTime, server_default=func.now(),
                            onupdate=func.now(), nullable=False)
    CreadoPor      = Column(Integer, nullable=False)

    especialidad = relationship("Especialidad")
    actividad    = relationship("Actividad")
```

---

## 4. Mock Data (JSON)

El archivo `backend/data/mock_data.json` simula la salida de la consulta SQL sobre el HIS de RELIV. La estructura replica exactamente los campos de la vista real, con dos campos adicionales críticos para el funcionamiento del sistema: `AgendamientoId` y `MedicoId`.

### 4.1 Campos del JSON y su origen

| Campo JSON | Origen SQL | Uso en el sistema |
|---|---|---|
| `AgendamientoId` | `AG.Id` | **Llave de enlace** con `Complemento_Parte_Diario` |
| `MedicoId` | `AG.MedicoId` *(campo pendiente de confirmar en HIS)* | Filtrado por doctor en el backend |
| `N_HC` | `PC.IDENTIFICACION` | Mostrar en tabla, solo lectura |
| `APELLIDOS` | `CONCAT(PC.PRIMERAPELLIDO, ' ', PC.SEGUNDOAPELLIDO)` | Mostrar en tabla, solo lectura |
| `NOMBRES` | `PC.NOMBRE` | Mostrar en tabla, solo lectura |
| `FECHA_NACIMIENTO` | `PC.FechaNacimiento` | Mostrar en tabla, solo lectura |
| `EDAD` | Calculada en SQL | Mostrar en tabla, solo lectura |
| `SEXO` | `CS.DESCRIPCION` | Mostrar en tabla, solo lectura |
| `CIE10` | `DP.CIE10_Codes` | Mostrar en tabla, solo lectura |
| `DIAGNOSTICO` | `DP.Diagnostico_Desc` | Mostrar en tabla, solo lectura |
| `PROCEDENCIA` | `PC.DIRECCION` | Mostrar en tabla, solo lectura |
| `CONVENIO` | `TC_CONV.Nombre` | Mostrar en tabla, solo lectura |

### 4.2 Archivo `mock_data.json`

```json
{
  "fuente": "mock",
  "fecha_consulta": "2026-06-27",
  "total_registros": 6,
  "pacientes": [
    {
      "AgendamientoId": 1001,
      "MedicoId": 10,
      "N_HC": "HC-2024-00451",
      "APELLIDOS": "Gutiérrez Mora",
      "NOMBRES": "Carmen Lucía",
      "FECHA_NACIMIENTO": "1968-03-15",
      "EDAD": 58,
      "SEXO": "Femenino",
      "CIE10": "C50.9",
      "DIAGNOSTICO": "Neoplasia maligna de mama, no especificada",
      "PROCEDENCIA": "Av. 6 de Diciembre N24-253, Quito",
      "CONVENIO": "IESS - Seguro General"
    },
    {
      "AgendamientoId": 1002,
      "MedicoId": 10,
      "N_HC": "HC-2023-01872",
      "APELLIDOS": "Paredes Villacís",
      "NOMBRES": "Roberto Andrés",
      "FECHA_NACIMIENTO": "1975-11-02",
      "EDAD": 50,
      "SEXO": "Masculino",
      "CIE10": "C34.1",
      "DIAGNOSTICO": "Neoplasia maligna del lóbulo superior, bronquio o pulmón",
      "PROCEDENCIA": "Calle Sucre 4-87, Latacunga",
      "CONVENIO": "Particular"
    },
    {
      "AgendamientoId": 1003,
      "MedicoId": 10,
      "N_HC": "HC-2025-00093",
      "APELLIDOS": "Mena Castillo",
      "NOMBRES": "Patricia Elena",
      "FECHA_NACIMIENTO": "1990-07-22",
      "EDAD": 35,
      "SEXO": "Femenino",
      "CIE10": "C53.9",
      "DIAGNOSTICO": "Neoplasia maligna del cuello uterino, no especificada",
      "PROCEDENCIA": "Urbanización Los Ceibos, Mz. 5 V. 12, Guayaquil",
      "CONVENIO": "Seguros Sucre - Plan Hospitalario"
    },
    {
      "AgendamientoId": 1004,
      "MedicoId": 11,
      "N_HC": "HC-2022-03341",
      "APELLIDOS": "Rivadeneira Toapanta",
      "NOMBRES": "Luis Humberto",
      "FECHA_NACIMIENTO": "1955-01-30",
      "EDAD": 71,
      "SEXO": "Masculino",
      "CIE10": "C61 ; C77.1",
      "DIAGNOSTICO": "Neoplasia maligna de próstata ; Ganglios linfáticos secundarios",
      "PROCEDENCIA": "Barrio San Juan, Calle Chimborazo 2-45, Riobamba",
      "CONVENIO": "IESS - Seguro Campesino"
    },
    {
      "AgendamientoId": 1005,
      "MedicoId": 11,
      "N_HC": "HC-2024-02210",
      "APELLIDOS": "Espinosa Naranjo",
      "NOMBRES": "Ana Sofía",
      "FECHA_NACIMIENTO": "1982-09-08",
      "EDAD": 43,
      "SEXO": "Femenino",
      "CIE10": "C83.3",
      "DIAGNOSTICO": "Linfoma difuso de células B grandes",
      "PROCEDENCIA": "Sector La Mariscal, Quito",
      "CONVENIO": "Medicina Prepagada Ecuasanitas"
    },
    {
      "AgendamientoId": 1006,
      "MedicoId": 12,
      "N_HC": "HC-2021-04589",
      "APELLIDOS": "Zambrano Ochoa",
      "NOMBRES": "Marco Vinicio",
      "FECHA_NACIMIENTO": "1948-05-17",
      "EDAD": 78,
      "SEXO": "Masculino",
      "CIE10": "C92.0",
      "DIAGNOSTICO": "Leucemia mieloide aguda",
      "PROCEDENCIA": "Av. Amazonas y Naciones Unidas, Quito",
      "CONVENIO": "Particular"
    }
  ]
}
```

> **Nota:** Los nombres, números de historia clínica y datos son completamente ficticios. Generados únicamente para pruebas de desarrollo.

---

## 5. Lógica del JOIN en Memoria (HIS + BD Local)

### 5.1 Concepto

Dado que los datos del HIS (mock o SQL real) y los complementos del médico viven en fuentes distintas, el backend realiza un **JOIN lógico en memoria** antes de entregar la respuesta al cliente. Este proceso ocurre dentro de `merge_service.py`.

```
Fuente A: HIS / mock_data.json
    → Lista de pacientes del día para un MedicoId
    → Llave: AgendamientoId

Fuente B: BD Local (Complemento_Parte_Diario)
    → Registros con campos complementarios ya guardados
    → Llave: AgendamientoId

JOIN en memoria (Python dict lookup O(1))
    → Un dict {AgendamientoId: complemento} construido desde Fuente B
    → Por cada paciente de Fuente A, se busca su complemento en el dict
    → Si existe → se adjunta; si no → los campos complementarios vienen como null

Resultado: Lista unificada de RegistroParteDiario (schema Pydantic)
```

### 5.2 Implementación

```python
# backend/services/merge_service.py

from typing import Optional
from sqlalchemy.orm import Session
from backend.models.complemento import ComplementoParteDiario
from backend.schemas.parte_diario import RegistroParteDiario, ComplementoSchema
from backend.services.his_service import obtener_pacientes_his
import datetime


def obtener_parte_diario_completo(
    db: Session,
    medico_id: int,
    fecha: datetime.date
) -> list[RegistroParteDiario]:
    """
    Une los datos del HIS con los complementos guardados en la BD local.
    Retorna la lista unificada lista para serializar al cliente.
    """

    # 1. Obtener pacientes del HIS (mock o SQL real)
    #    Filtrados por medico_id y fecha
    pacientes_his = obtener_pacientes_his(medico_id=medico_id, fecha=fecha)

    if not pacientes_his:
        return []

    # 2. Extraer los AgendamientoIds presentes en esta agenda
    agendamiento_ids = [p["AgendamientoId"] for p in pacientes_his]

    # 3. Consultar en BD local SOLO los complementos de esta agenda
    complementos_raw = (
        db.query(ComplementoParteDiario)
        .filter(ComplementoParteDiario.AgendamientoId.in_(agendamiento_ids))
        .all()
    )

    # 4. Construir dict para lookup O(1): {AgendamientoId: complemento_orm}
    complementos_dict: dict[int, ComplementoParteDiario] = {
        c.AgendamientoId: c for c in complementos_raw
    }

    # 5. Unir: por cada paciente del HIS, adjuntar su complemento (si existe)
    resultado: list[RegistroParteDiario] = []

    for paciente in pacientes_his:
        ag_id = paciente["AgendamientoId"]
        complemento = complementos_dict.get(ag_id)

        registro = RegistroParteDiario(
            # Campos del HIS (solo lectura)
            AgendamientoId   = ag_id,
            MedicoId         = paciente["MedicoId"],
            N_HC             = paciente["N_HC"],
            Apellidos        = paciente["APELLIDOS"],
            Nombres          = paciente["NOMBRES"],
            FechaNacimiento  = paciente["FECHA_NACIMIENTO"],
            Edad             = paciente["EDAD"],
            Sexo             = paciente["SEXO"],
            CIE10            = paciente["CIE10"],
            Diagnostico      = paciente["DIAGNOSTICO"],
            Procedencia      = paciente["PROCEDENCIA"],
            Convenio         = paciente["CONVENIO"],

            # Estado del complemento
            ComplementoCompleto = complemento is not None,

            # Campos complementarios (None si el médico aún no los llenó)
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
```

### 5.3 Schema Pydantic del registro unificado

```python
# backend/schemas/parte_diario.py

from pydantic import BaseModel
from typing import Optional
import datetime


class ComplementoSchema(BaseModel):
    EspecialidadId : int
    ActividadId    : int
    TipoConsulta   : str   # 'PRIMERA_VEZ' | 'SUBSECUENTE'
    Pre_QT         : bool
    Pre_QX         : bool
    Quimio         : bool
    EKG            : bool


class RegistroParteDiario(BaseModel):
    # Datos HIS — solo lectura en el cliente
    AgendamientoId   : int
    MedicoId         : int
    N_HC             : str
    Apellidos        : str
    Nombres          : str
    FechaNacimiento  : str
    Edad             : int
    Sexo             : str
    CIE10            : Optional[str] = None
    Diagnostico      : Optional[str] = None
    Procedencia      : Optional[str] = None
    Convenio         : Optional[str] = None

    # Metadato útil para que el frontend muestre el estado de completitud
    ComplementoCompleto : bool = False

    # Datos locales — editables por el médico; null si aún no se han llenado
    Complemento : Optional[ComplementoSchema] = None

    class Config:
        from_attributes = True
```

### 5.4 Servicio HIS (capa de abstracción)

```python
# backend/services/his_service.py
"""
Capa de abstracción sobre la fuente de datos del HIS.
En desarrollo: lee mock_data.json.
En producción: ejecuta la consulta SQL contra RELIV.
El resto del sistema nunca distingue entre las dos fuentes.
"""

import json
import datetime
from pathlib import Path

MOCK_PATH = Path(__file__).parent.parent / "data" / "mock_data.json"


def obtener_pacientes_his(
    medico_id: int,
    fecha: datetime.date
) -> list[dict]:
    """
    Retorna la lista de pacientes del HIS filtrada por médico y fecha.
    Cambia SOLO esta función al conectar con SQL Server real.
    """
    # --- Modo mock (temporal) ---
    with open(MOCK_PATH, encoding="utf-8") as f:
        data = json.load(f)

    return [
        p for p in data["pacientes"]
        if p["MedicoId"] == medico_id
        # En el mock no filtramos por fecha (todos son del día de hoy)
        # En producción, la query SQL ya filtra por CAST(AG.Fecha AS DATE) = :fecha
    ]

    # --- Modo producción (descomentar al tener acceso al HIS) ---
    # from backend.database import his_engine
    # from sqlalchemy import text
    # with his_engine.connect() as conn:
    #     result = conn.execute(
    #         text("""
    #             SELECT AG.Id AS AgendamientoId, AG.MedicoId, PC.IDENTIFICACION AS N_HC,
    #                    ... (query completa del documento 01)
    #             WHERE CAST(AG.Fecha AS DATE) = :fecha
    #               AND AG.MedicoId = :medico_id
    #         """),
    #         {"fecha": fecha, "medico_id": medico_id}
    #     )
    #     return [dict(row) for row in result.mappings()]
```

---

## 6. Endpoints Principales de la API

| Método | Ruta | Descripción | Rol permitido |
|---|---|---|---|
| `POST` | `/auth/login` | Autenticación, retorna JWT | Todos |
| `GET` | `/agenda/dia?fecha=YYYY-MM-DD` | Parte diario del médico autenticado (JOIN completo) | Doctor |
| `GET` | `/agenda/global?medico_id=&fecha_inicio=&fecha_fin=` | Vista global con filtros | Enfermero |
| `PUT` | `/complemento/{agendamiento_id}` | Guardar o actualizar campos complementarios | Doctor |
| `GET` | `/catalogos/especialidades` | Lista de especialidades activas | Doctor |
| `GET` | `/catalogos/actividades/{especialidad_id}` | Actividades de una especialidad | Doctor |
| `GET` | `/exportar/pdf?fecha=&medico_id=` | Descarga el parte diario en PDF | Doctor / Enfermero |
| `GET` | `/exportar/excel?fecha=&medico_id=` | Descarga el parte diario en Excel | Doctor / Enfermero |
| `GET` | `/concentrado/mensual?anio=&mes=&medico_ids=` | Concentrado mensual consolidado | Enfermero |
| `GET` | `/concentrado/mensual/exportar` | Descarga el concentrado en Excel | Enfermero |

---

## 7. Flujo de Guardado Automático (Auto-save)

```
Frontend (Doctor edita un campo)
    │
    │  Evento onBlur o onChange con debounce (500ms)
    ▼
PUT /complemento/{agendamiento_id}
    Body: { EspecialidadId, ActividadId, TipoConsulta, Pre_QT, Pre_QX, Quimio, EKG }
    Header: Authorization: Bearer <JWT>
    │
    │  Backend valida JWT, extrae medico_id del token
    │  Verifica que el AgendamientoId pertenezca a ese medico_id (seguridad)
    ▼
UPSERT en Complemento_Parte_Diario
    -- SQLite:    INSERT OR REPLACE INTO ...
    -- PostgreSQL: INSERT ... ON CONFLICT (AgendamientoId) DO UPDATE SET ...
    │
    ▼
HTTP 200 { "guardado": true, "AgendamientoId": 1001 }
    │
    ▼
Frontend muestra indicador "✓ Guardado" por 2 segundos (sin modal, sin bloqueo)
```

---

## 8. Variables de Entorno (`.env`)

```ini
# Entorno
APP_ENV=development          # development | production

# BD local
DATABASE_URL=sqlite:///./solca_parte_diario.db
# DATABASE_URL=postgresql://usuario:clave@localhost:5432/solca_parte_diario

# JWT
SECRET_KEY=cambia_esta_clave_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480   # 8 horas (jornada laboral)

# HIS (para producción)
HIS_DB_SERVER=servidor-sql-solca
HIS_DB_NAME=RELIV
HIS_DB_USER=usuario_lectura
HIS_DB_PASSWORD=contraseña_segura

# Fuente de datos activa
HIS_DATA_SOURCE=mock    # mock | sql
```

---

## 9. Diagrama Entidad-Relación (BD Local)

```
┌──────────────┐        ┌──────────────────────────┐        ┌───────────────┐
│ Especialidad │        │  Complemento_Parte_Diario │        │   Actividad   │
├──────────────┤        ├──────────────────────────┤        ├───────────────┤
│ Id (PK)      │◄───────│ EspecialidadId (FK)       │        │ Id (PK)       │
│ Nombre       │        │ ActividadId    (FK)  ──────────────►│ EspecialidadId│
│ Activa       │        │                           │        │ Nombre        │
└──────────────┘        │ Id (PK)                   │        │ Activa        │
                        │ AgendamientoId (UNIQUE)   │        └───────────────┘
                        │ MedicoId                  │
                        │ FechaParte                │   ← AgendamientoId es la
                        │ TipoConsulta              │     llave de enlace lógica
                        │ Pre_QT                    │     con la vista HIS de RELIV
                        │ Pre_QX                    │     (no FK física porque son
                        │ Quimio                    │     sistemas distintos)
                        │ EKG                       │
                        │ CreadoEn                  │
                        │ ActualizadoEn             │
                        │ CreadoPor                 │
                        └──────────────────────────┘
```

---

## 10. Notas de Migración a Producción

- **Paso 1 — Conexión SQL:** modificar únicamente `his_service.py`, cambiando `HIS_DATA_SOURCE=mock` por `HIS_DATA_SOURCE=sql` en el `.env` y configurando las credenciales de RELIV.
- **Paso 2 — BD local:** cambiar `DATABASE_URL` de SQLite a PostgreSQL. Ejecutar `alembic upgrade head` para aplicar el esquema en el servidor.
- **Paso 3 — Confirmar campo `MedicoId`:** verificar con el equipo de RELIV el nombre exacto de la columna que identifica al médico responsable en `AgendamientoSolcaT` para alinear el filtrado.
- **Paso 4 — HTTPS:** desplegar detrás de un proxy inverso (Nginx) con certificado TLS para cifrar el tráfico del JWT y los datos clínicos.

---

*Documento elaborado por el equipo de Arquitectura de Datos. Para consultas técnicas, referirse al líder de backend del proyecto.*
