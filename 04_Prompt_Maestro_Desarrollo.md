# 04 — Prompt Maestro de Desarrollo
## Sistema de Parte Diario Médico — SOLCA

> **Uso:** Copiar todo el contenido del bloque de prompt y pegarlo en Cursor, Claude Code, GitHub Copilot Chat o cualquier IA de generación de código.  
> **Dependencias:** Documentos `01`, `02` y `03` de esta serie.  
> **Resultado esperado:** Aplicación funcional completa lista para ejecutar con `uvicorn` y abrir en el navegador.

---

## ══════════════════════════════════════════════
## INICIO DEL PROMPT MAESTRO — COPIAR DESDE AQUÍ
## ══════════════════════════════════════════════

```
Eres un Tech Lead Senior experto en Python, FastAPI, SQLAlchemy y desarrollo
frontend con HTML/CSS/JavaScript vanilla. Vas a construir desde cero el
"Sistema de Parte Diario Médico" para SOLCA (Sociedad de Lucha Contra el
Cáncer). Lee TODAS las instrucciones antes de escribir una sola línea de
código. Sigue el orden indicado sin saltarte pasos.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REGLAS ABSOLUTAS — NUNCA LAS VIOLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

R1. Genera TODOS los archivos en una sola respuesta, en orden, con sus
    rutas exactas como encabezado de bloque de código.
    Ejemplo:  # === backend/main.py ===

R2. NO uses librerías que no estén en la lista de dependencias aprobadas.
    NO instales React, Next.js, ni ningún framework JS pesado.
    El frontend es HTML + CSS + JavaScript vanilla en una sola carpeta.

R3. El backend NUNCA intenta conectarse a SQL Server. Todo dato de
    pacientes viene de mock_data.json. La conexión SQL se habilitará
    después; deja el código preparado pero comentado.

R4. La base de datos local será MySQL (usando Laragon). Asegúrate de usar el driver pymysql para SQLAlchemy.

R5. Todos los colores de la interfaz deben respetar la paleta SOLCA:
    - Azul oscuro:  #003366  (navbar, encabezados, botones primarios)
    - Blanco:       #FFFFFF  (fondo de toda la aplicación)
    - Gris claro:   #F5F7FA  (filas alternas de tablas)
    - Verde:        #27AE60  (indicador de fila completa / guardado)
    - Rojo error:   #C0392B
    - Borde:        #D0D7DE
    NO uses otros colores. Si dudas entre dos opciones, usa el azul oscuro.

R6. CERO modales innecesarios. Ninguna ventana emergente de confirmación
    para acciones cotidianas (guardar, cambiar especialidad, cambiar de
    fila). La única excepción permitida es el logout.

R7. El guardado de complementos es automático (auto-save con debounce de
    500ms al perder el foco de cualquier campo editable). Sin botón de
    "Guardar" explícito en la tabla. El indicador de guardado es texto
    pequeño "✓ Guardado" que aparece 2 segundos y desaparece.

R8. La seguridad de roles se implementa en el BACKEND, no solo en el
    frontend. Un doctor nunca puede ver datos de otro doctor aunque
    manipule la URL o el token.

R9. Genera código limpio, comentado en español, con nombres de variables
    descriptivos. Cada archivo debe tener un comentario de cabecera que
    explique su propósito.

R10. Al final, genera un archivo README.md con los comandos exactos para
     levantar el sistema desde cero en menos de 5 minutos.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STACK TECNOLÓGICO APROBADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backend:
  - Python 3.11+
  - FastAPI 0.111.0
  - Uvicorn 0.29.0  (servidor ASGI)
  - SQLAlchemy 2.0.30  (ORM)
  - Alembic 1.13.1  (migraciones)
  - python-jose[cryptography] 3.3.0  (JWT)
  - passlib[bcrypt] 1.7.4  (hashing de contraseñas)
  - pydantic 2.7.1
  - pydantic-settings 2.2.1
  - python-multipart 0.0.9
  - reportlab 4.2.0  (generación de PDF)
  - openpyxl 3.1.2  (generación de Excel)

Frontend:
  - HTML5 + CSS3 + JavaScript ES6+ (vanilla, SIN frameworks)
  - Fetch API nativa para llamadas al backend
  - Sin dependencias npm. Sin node_modules. Sin bundlers.
  - Un archivo HTML por vista, CSS compartido en un archivo.

Base de datos:
  - SQLite  (archivo: solca_parte_diario.db en la raíz del proyecto)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESTRUCTURA DE CARPETAS — CREA EXACTAMENTE ESTA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

solca-parte-diario/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── complemento.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── catalogo.py
│   │   ├── complemento.py
│   │   └── parte_diario.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── agenda.py
│   │   ├── catalogos.py
│   │   ├── complemento.py
│   │   ├── exportacion.py
│   │   └── concentrado.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── his_service.py
│   │   ├── merge_service.py
│   │   └── export_service.py
│   │
│   └── data/
│       ├── mock_data.json
│       └── usuarios_dev.json
│
├── frontend/
│   ├── index.html          (login)
│   ├── doctor.html         (vista del médico)
│   ├── enfermero.html      (vista global)
│   ├── css/
│   │   └── solca.css       (estilos globales + paleta SOLCA)
│   └── js/
│       ├── auth.js         (manejo de JWT en memoria)
│       ├── api.js          (wrapper Fetch con token)
│       ├── doctor.js       (lógica de la vista del médico)
│       └── enfermero.js    (lógica de la vista del enfermero)
│
├── migrations/             (Alembic)
│   └── versions/
│
├── .env
├── .gitignore
├── alembic.ini
├── requirements.txt
├── seed.py
└── README.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 1 DE N: requirements.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Genera requirements.txt con todas las dependencias listadas en el
stack tecnológico aprobado, con versiones exactas fijadas.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 2 DE N: .env
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Genera el archivo .env con estas variables exactas:

  APP_ENV=development
  DATABASE_URL=mysql+pymysql://root:@localhost/solca_parte_diario
  SECRET_KEY=solca-dev-secret-key-cambiar-en-produccion
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=480
  HIS_DATA_SOURCE=mock

  # Variables para producción SQL Server (comentadas)
  # HIS_DB_SERVER=servidor-sql-solca
  # HIS_DB_NAME=RELIV
  # HIS_DB_USER=usuario_lectura
  # HIS_DB_PASSWORD=contraseña_segura

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 3 DE N: backend/data/mock_data.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Genera este JSON EXACTAMENTE con esta estructura y estos 6 registros.
No cambies ningún campo ni valor. Este archivo simula la salida de la
consulta SQL sobre el HIS de RELIV.

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
      "PROCEDENCIA": "Urbanización Los Ceibos, Guayaquil",
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
      "PROCEDENCIA": "Calle Chimborazo 2-45, Riobamba",
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

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 4 DE N: backend/data/usuarios_dev.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Genera usuarios_dev.json con 3 usuarios de prueba:
- dr.gutierrez  / Solca2026!  / rol: doctor   / medico_id: 10
- dr.paredes    / Solca2026!  / rol: doctor   / medico_id: 11
- enf.torres    / Solca2026!  / rol: enfermero / medico_id: null

Genera los hashes bcrypt de la contraseña "Solca2026!" usando passlib
y úsalos en el JSON. No pongas la contraseña en texto plano.

Estructura de cada usuario:
{
  "id": <int>,
  "username": "<string>",
  "password_hash": "<bcrypt_hash>",
  "rol": "doctor" | "enfermero",
  "nombre_completo": "<string>",
  "medico_id": <int> | null
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 5 DE N: backend/config.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Usa pydantic-settings BaseSettings. Lee todas las variables del .env.
Exporta una instancia singleton llamada `settings`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 6 DE N: backend/database.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Crea:
- engine SQLAlchemy para SQLite con check_same_thread=False
- SessionLocal con autocommit=False, autoflush=False
- Clase Base declarativa
- Función generadora get_db() para inyección de dependencias FastAPI
- Deja comentado (pero presente) el código para crear his_engine
  conectando a SQL Server vía pyodbc cuando HIS_DATA_SOURCE == "sql"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 7 DE N: backend/models/complemento.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Define 3 modelos ORM con SQLAlchemy 2.x:

MODELO 1 — Especialidad:
  Columnas: Id (PK autoincrement), Nombre (VARCHAR 80, unique),
            Activa (Boolean, default True)
  Relación: one-to-many con Actividad

MODELO 2 — Actividad:
  Columnas: Id (PK autoincrement), EspecialidadId (FK → Especialidad.Id),
            Nombre (VARCHAR 100), Activa (Boolean, default True)
  Relación: many-to-one con Especialidad
  Índice: en EspecialidadId

MODELO 3 — ComplementoParteDiario:
  Columnas:
    Id             INTEGER  PK autoincrement
    AgendamientoId INTEGER  NOT NULL UNIQUE  ← llave de enlace con el HIS
    MedicoId       INTEGER  NOT NULL
    FechaParte     DATE     NOT NULL
    EspecialidadId INTEGER  FK → Especialidad.Id
    ActividadId    INTEGER  FK → Actividad.Id
    TipoConsulta   VARCHAR(15)  CHECK IN ('PRIMERA_VEZ','SUBSECUENTE')
    Pre_QT         BOOLEAN  default False
    Pre_QX         BOOLEAN  default False
    Quimio         BOOLEAN  default False
    EKG            BOOLEAN  default False
    CreadoEn       DATETIME default now()
    ActualizadoEn  DATETIME default now(), onupdate now()
    CreadoPor      INTEGER  NOT NULL

  Índices: (MedicoId, FechaParte) y (FechaParte)
  Constraint: UniqueConstraint en AgendamientoId
  Relaciones: many-to-one con Especialidad y Actividad

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 8 DE N: backend/schemas/ (todos los schemas Pydantic)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

backend/schemas/auth.py:
  - LoginInput: username (str), password (str)
  - TokenOutput: access_token (str), token_type (str), rol (str),
                 nombre_completo (str), medico_id (int | None)

backend/schemas/catalogo.py:
  - EspecialidadOut: Id (int), Nombre (str)
  - ActividadOut: Id (int), EspecialidadId (int), Nombre (str)

backend/schemas/complemento.py:
  - ComplementoInput:
      EspecialidadId (int), ActividadId (int),
      TipoConsulta (Literal["PRIMERA_VEZ","SUBSECUENTE"]),
      Pre_QT (bool, default False), Pre_QX (bool, default False),
      Quimio (bool, default False), EKG (bool, default False)
  - ComplementoOutput hereda ComplementoInput y agrega:
      Id (int), AgendamientoId (int), MedicoId (int), FechaParte (str)
      Config: from_attributes = True

backend/schemas/parte_diario.py:
  - ComplementoSchema: igual que ComplementoInput pero todos opcionales
  - RegistroParteDiario:
      AgendamientoId (int), MedicoId (int),
      N_HC (str), Apellidos (str), Nombres (str),
      FechaNacimiento (str), Edad (int), Sexo (str),
      CIE10 (str | None), Diagnostico (str | None),
      Procedencia (str | None), Convenio (str | None),
      ComplementoCompleto (bool, default False),
      Complemento (ComplementoSchema | None, default None)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 9 DE N: backend/services/his_service.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Implementa la función pública:
  obtener_pacientes_his(medico_id: int, fecha: date) -> list[dict]

Lógica:
  1. Leer settings.HIS_DATA_SOURCE
  2. Si es "mock":
     - Abrir backend/data/mock_data.json
     - Filtrar registros donde paciente["MedicoId"] == medico_id
     - Retornar la lista filtrada
  3. Si es "sql":
     - Ejecutar la siguiente query parametrizada contra his_engine
       (que viene de database.py):

       SELECT
           AG.Id AS AgendamientoId,
           AG.MedicoId AS MedicoId,
           PC.IDENTIFICACION AS N_HC,
           CONCAT(PC.PRIMERAPELLIDO,' ',PC.SEGUNDOAPELLIDO) AS APELLIDOS,
           PC.NOMBRE AS NOMBRES,
           CAST(PC.FechaNacimiento AS DATE) AS FECHA_NACIMIENTO,
           FLOOR(DATEDIFF(DAY,PC.FechaNacimiento,GETDATE())/365.25) AS EDAD,
           CS.DESCRIPCION AS SEXO,
           DP.CIE10_Codes AS CIE10,
           DP.Diagnostico_Desc AS DIAGNOSTICO,
           PC.DIRECCION AS PROCEDENCIA,
           TC_CONV.Nombre AS CONVENIO
       FROM [dbo].[AgendamientoSolcaT] AG
       INNER JOIN [dbo].[PacientesSolcaT] PC ON AG.PacienteId = PC.ID
       INNER JOIN [dbo].[AdmisionesSolcaT] AD ON AG.Id = AD.AgendandamientoId
       INNER JOIN [dbo].[EnfermedadActualSolcaT] EA ON AD.Codigo = EA.CódigoAdmisión
       LEFT JOIN [dbo].[TipoCategoria] CS ON PC.SEXOID = CS.Id
       LEFT JOIN [dbo].[AdmisionesSeguroSolcaT] ADS ON AD.Id = ADS.AdmissionId
       LEFT JOIN [dbo].[ConveniosSolcaT] TC_CONV ON ADS.ConvenioId = TC_CONV.Id
       OUTER APPLY (
           SELECT
               STRING_AGG(C.Codigo, ' ; ') AS CIE10_Codes,
               STRING_AGG(C.Descripcion, ' ; ') AS Diagnostico_Desc
           FROM (
               SELECT LTRIM(RTRIM(REPLACE(REPLACE(
                      value,CHAR(13),''),CHAR(10),''))) AS CleanValue
               FROM STRING_SPLIT(EA.DiagnósticosCIE10, ';')
           ) AS S
           CROSS APPLY (
               SELECT CASE WHEN CHARINDEX(' - ',S.CleanValue)>0
                      THEN LTRIM(RTRIM(LEFT(S.CleanValue,
                           CHARINDEX(' - ',S.CleanValue)-1)))
                      ELSE S.CleanValue END AS CodigoExtraido
           ) AS Ext
           LEFT JOIN [dbo].[Cie10] C ON Ext.CodigoExtraido = C.Codigo
           WHERE S.CleanValue <> ''
       ) AS DP
       WHERE EA.DiagnósticosCIE10 IS NOT NULL
         AND CAST(AG.Fecha AS DATE) = :fecha
         AND AG.MedicoId = :medico_id
       ORDER BY AG.Fecha ASC

     - Retornar lista de dicts

  Para el modo "sql", envuelve TODO en un bloque try/except. Si falla
  la conexión, lanza HTTPException 503 con mensaje claro.

  Incluye también:
    obtener_todos_pacientes_his(fecha_inicio, fecha_fin, medico_id=None)
  para el enfermero. En modo mock retorna todos los registros
  (opcionalmente filtrados por medico_id si se provee).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 10 DE N: backend/services/merge_service.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Implementa:

  obtener_parte_diario_completo(
      db: Session, medico_id: int, fecha: date
  ) -> list[RegistroParteDiario]

  Algoritmo exacto:
  1. Llamar a his_service.obtener_pacientes_his(medico_id, fecha)
  2. Si la lista está vacía, retornar []
  3. Extraer todos los AgendamientoIds de la lista
  4. Consultar BD local: SELECT * FROM Complemento_Parte_Diario
     WHERE AgendamientoId IN (<ids>)
  5. Construir dict Python: {AgendamientoId: complemento_orm}
     para lookup O(1)
  6. Por cada paciente del HIS:
     - Buscar su complemento en el dict
     - Construir RegistroParteDiario con campos HIS + Complemento
     - ComplementoCompleto = True si existe el complemento, False si no
  7. Retornar la lista resultante

  Implementa también:
    obtener_concentrado(
        db: Session,
        fecha_inicio: date,
        fecha_fin: date,
        medico_ids: list[int] | None = None
    ) -> list[RegistroParteDiario]
  Para el Concentrado Mensual del enfermero.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 11 DE N: backend/routers/auth.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Implementa:

  POST /auth/login
    - Recibe LoginInput (username, password)
    - Carga usuarios_dev.json
    - Busca el usuario por username
    - Verifica password con passlib bcrypt
    - Si válido: crea JWT con payload:
        { "sub": str(user.id), "rol": rol, "medico_id": medico_id,
          "nombre_completo": nombre_completo }
    - Retorna TokenOutput
    - Si inválido: HTTPException 401 con message genérico
      "Credenciales incorrectas" (no especifica cuál campo falló)

  Función get_current_user(token: str = Depends(oauth2_scheme))
    - Decodifica y valida el JWT
    - Retorna el payload como dict
    - Si el token es inválido o expiró: HTTPException 401

  Exporta get_current_user para ser usada como dependencia
  en todos los demás routers.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 12 DE N: backend/routers/agenda.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GET /agenda/dia
  Parámetro: fecha (date, default hoy)
  Solo rol "doctor". Si el rol es otro: 403.
  Extrae medico_id del token JWT (no del query string).
  Llama a merge_service.obtener_parte_diario_completo()
  Retorna list[RegistroParteDiario]

GET /agenda/global
  Parámetros: fecha_inicio (date), fecha_fin (date),
              medico_id (int, opcional)
  Solo rol "enfermero". Si el rol es otro: 403.
  Llama a merge_service.obtener_concentrado()
  Retorna list[RegistroParteDiario]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 13 DE N: backend/routers/catalogos.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GET /catalogos/especialidades
  Requiere JWT válido (cualquier rol).
  Retorna todas las Especialidades con Activa=True
  ordenadas por Nombre.

GET /catalogos/actividades/{especialidad_id}
  Requiere JWT válido (cualquier rol).
  Retorna todas las Actividades de esa especialidad con Activa=True.
  Si especialidad_id no existe: retorna lista vacía (no error 404).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 14 DE N: backend/routers/complemento.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PUT /complemento/{agendamiento_id}
  Solo rol "doctor". Si rol es otro: 403.
  Recibe ComplementoInput como body.

  Lógica de seguridad OBLIGATORIA:
    1. Extraer medico_id del token JWT
    2. Obtener los pacientes del día del médico desde his_service
    3. Verificar que agendamiento_id está en esa lista
    4. Si NO está: HTTPException 403 "Agendamiento no pertenece
       al médico autenticado"
    5. Si SÍ está: hacer UPSERT en Complemento_Parte_Diario

  UPSERT:
    - Buscar registro existente por AgendamientoId
    - Si existe: actualizar todos los campos del payload
    - Si no existe: crear nuevo registro con AgendamientoId,
      MedicoId (del token), FechaParte (hoy), CreadoPor (user.id)
    - db.commit(), db.refresh()
    - Retornar ComplementoOutput

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 15 DE N: backend/services/export_service.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Implementa con ReportLab y openpyxl:

FUNCIÓN 1: generar_pdf_parte_diario(registros, medico_nombre, fecha) -> bytes
  - Orientación: landscape (horizontal)
  - Encabezado: texto "SOCIEDAD DE LUCHA CONTRA EL CÁNCER — SOLCA"
    en negro, luego "Parte Diario Médico" en azul #003366
  - Línea separadora color #003366
  - Datos: Médico: [nombre]   Fecha: [DD/MM/YYYY]
  - Tabla de pacientes con estas columnas:
    N°HC | Apellidos y Nombres | Edad | Sexo | CIE10 |
    Diagnóstico | Convenio | Especialidad | Actividad |
    Tipo | QT | QX | Quimio | EKG
  - Encabezado de tabla: fondo #003366, texto blanco, bold, 8pt
  - Filas alternas: blanco y #F5F7FA, texto 7pt
  - Checkboxes: "✓" si True, "" si False
  - Fila de totales al pie: suma de cada columna booleana
  - Pie de página: "Generado el [fecha hora] — Sistema Parte Diario SOLCA"
    y número de página
  - Retorna bytes del PDF (sin guardar en disco)

FUNCIÓN 2: generar_excel_parte_diario(registros, medico_nombre, fecha) -> bytes
  - Una hoja: "Parte Diario"
  - Fila 1: "SOLCA — Parte Diario Médico" (merge columnas, 14pt bold, #003366)
  - Fila 2: "Médico: [nombre]   |   Fecha: [fecha]"
  - Fila 3: vacía
  - Fila 4: encabezados (fondo #003366, fuente blanca, bold, bordes)
  - Filas 5+: datos (filas alternas blanco/#F5F7FA)
  - Checkboxes: "SÍ" si True, "" si False
  - Última fila: TOTALES con suma de cada columna numérica/booleana
  - Auto-ajustar ancho de columnas
  - Retorna bytes (sin guardar en disco)

FUNCIÓN 3: generar_excel_concentrado(registros, fecha_inicio, fecha_fin) -> bytes
  - Tres hojas:
    Hoja "Detalle": una fila por paciente con todos los campos
    Hoja "Por Médico": agrupado por MedicoId, con totales por fila
                       y fila TOTAL GENERAL al pie (fondo #003366, blanco)
    Hoja "Por Especialidad": agrupado por especialidad, con totales
  - Retorna bytes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 16 DE N: backend/routers/exportacion.py y concentrado.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

exportacion.py:
  GET /exportar/pdf
    Params: fecha (date, default hoy)
    Solo doctor. Llama a merge_service + export_service.generar_pdf.
    Retorna Response con media_type="application/pdf"
    y header Content-Disposition con nombre de archivo descriptivo.

  GET /exportar/excel
    Params: fecha (date, default hoy)
    Solo doctor. Retorna .xlsx como StreamingResponse.

concentrado.py:
  GET /concentrado/mensual/exportar
    Params: fecha_inicio, fecha_fin, medico_ids (str opcional "10,11,12")
    Solo enfermero.
    Parsea medico_ids a list[int] si se provee.
    Llama a merge_service.obtener_concentrado()
    Llama a export_service.generar_excel_concentrado()
    Retorna StreamingResponse con el .xlsx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 17 DE N: backend/main.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Crea la aplicación FastAPI con:
  - Título: "SOLCA - Sistema de Parte Diario Médico"
  - docs_url="/api/docs", redoc_url="/api/redoc"
  - CORS middleware permitiendo localhost:5500, localhost:8080,
    localhost:3000 y localhost:5173 (para desarrollo con Live Server)
  - Registro de todos los routers con sus prefijos:
      /auth, /agenda, /catalogos, /complemento, /exportar, /concentrado
  - GET /health que retorna {"status": "ok", "version": "1.0.0"}
  - Evento startup que crea las tablas si no existen:
      Base.metadata.create_all(bind=engine)
    y llama a seed() si las tablas están vacías

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO 18 DE N: seed.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Script independiente ejecutable con: python seed.py

Debe:
  1. Crear todas las tablas (si no existen)
  2. Verificar si ya hay datos en Especialidad; si sí, salir sin hacer nada
  3. Insertar las 6 especialidades:
     Oncología Médica, Oncología Quirúrgica, Radioterapia,
     Hematología, Cardiología, Medicina Interna
  4. Insertar las actividades correspondientes a cada especialidad
     (las del documento de arquitectura, sección 3.2)
  5. Imprimir confirmación al final: "✓ Semilla aplicada: X especialidades,
     Y actividades"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVOS 19–22 DE N: FRONTEND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANTE: El frontend es HTML+CSS+JS vanilla.
El backend sirve los archivos HTML directamente usando
FastAPI StaticFiles o el desarrollador abre con Live Server.
El puerto del backend es 8000. Todas las llamadas a la API
van a http://localhost:8000.

── frontend/css/solca.css ──────────────────────────

Define las siguientes variables CSS y estilos globales:

:root {
  --azul:        #003366;
  --blanco:      #FFFFFF;
  --fila-alt:    #F5F7FA;
  --verde:       #27AE60;
  --rojo:        #C0392B;
  --borde:       #D0D7DE;
  --texto:       #2C2C2C;
}

Estilos requeridos (cada uno con su selector y propiedades completas):
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: Arial, sans-serif; }
  body { background: var(--blanco); color: var(--texto); }

  .navbar:
    background: var(--azul), color: blanco, padding 12px 24px,
    display flex, justify-content space-between, align-items center,
    font-size 15px

  .navbar .logo: font-weight bold, font-size 18px
  .navbar .user-info: display flex, gap 16px, align-items center

  .btn-primary:
    background var(--azul), color blanco, border none,
    padding 8px 20px, border-radius 4px, cursor pointer, font-size 14px
  .btn-primary:hover: background #004080

  .btn-secondary:
    background blanco, color var(--azul),
    border 1.5px solid var(--azul), padding 8px 20px,
    border-radius 4px, cursor pointer, font-size 14px
  .btn-secondary:hover: background #F0F4F8

  .btn-small: igual que btn-primary pero padding 4px 12px, font-size 12px

  .table-container: overflow-x auto, margin-top 16px

  table.agenda:
    width 100%, border-collapse collapse, font-size 13px

  table.agenda thead tr:
    background var(--azul), color blanco

  table.agenda thead th:
    padding 10px 8px, text-align left, font-weight bold,
    border 1px solid #2a5a9f, white-space nowrap

  table.agenda tbody tr:nth-child(even):
    background var(--fila-alt)

  table.agenda tbody tr.completa:
    border-left: 3px solid var(--verde)

  table.agenda tbody td:
    padding 8px, border 1px solid var(--borde), vertical-align middle

  select.celda-select:
    width 100%, border 1px solid var(--borde), padding 4px,
    font-size 12px, border-radius 3px, background blanco

  input[type=checkbox].celda-check:
    width 18px, height 18px, cursor pointer, accent-color var(--azul)

  .indicador-guardado:
    font-size 11px, color var(--verde), font-weight bold,
    opacity 0, transition opacity 0.3s

  .indicador-guardado.visible: opacity 1

  .filtros-bar:
    background var(--fila-alt), padding 12px 24px,
    border-bottom 1px solid var(--borde),
    display flex, gap 16px, align-items center, flex-wrap wrap

  .filtros-bar label: font-size 13px, color var(--texto)

  .filtros-bar input[type=date]:
    border 1px solid var(--borde), padding 6px 10px,
    border-radius 4px, font-size 13px

  .panel-main: padding 24px

  .login-container:
    min-height 100vh, display flex, align-items center,
    justify-content center, background var(--blanco)

  .login-card:
    width 360px, padding 40px, border 1px solid var(--borde),
    border-radius 8px, box-shadow 0 2px 12px rgba(0,0,0,0.08)

  .login-titulo:
    color var(--azul), font-size 22px, font-weight bold,
    text-align center, margin-bottom 8px

  .login-subtitulo:
    color #666, font-size 13px, text-align center, margin-bottom 28px

  .form-group: margin-bottom 16px
  .form-group label: display block, font-size 13px, margin-bottom 4px,
                     color var(--texto), font-weight 500
  .form-group input:
    width 100%, padding 10px 12px, border 1px solid var(--borde),
    border-radius 4px, font-size 14px, outline none
  .form-group input:focus: border-color var(--azul)

  .error-msg: color var(--rojo), font-size 12px, margin-top 8px,
              display none
  .error-msg.visible: display block

  .resumen-bar:
    background var(--fila-alt), padding 8px 24px,
    border-bottom 1px solid var(--borde),
    font-size 13px, color var(--texto), display flex, gap 24px

  .badge-completo: color var(--verde), font-weight bold
  .badge-pendiente: color #E67E22, font-weight bold

── frontend/index.html (LOGIN) ────────────────────

Estructura:
  <!DOCTYPE html> con lang="es", charset UTF-8, viewport mobile-first
  <title>SOLCA — Iniciar Sesión</title>
  <link> al css/solca.css

  Body con clase login-container:
    Div login-card:
      Logo: texto "SOLCA" en grande azul (o tag <img> con alt si hay logo)
      H1 clase login-titulo: "Parte Diario Médico"
      P clase login-subtitulo: "Sociedad de Lucha Contra el Cáncer"
      Form id="form-login" (sin action, manejado por JS):
        Campo Usuario (label + input type=text id="username" autocomplete=username)
        Campo Contraseña (label + input type=password id="password")
        Botón type=submit clase btn-primary ancho 100%: "Ingresar"
        P clase error-msg id="error-msg"
      P pequeño al pie: versión "v1.0.0 — Desarrollo"
  <script src="js/auth.js">

  Comportamiento JS en auth.js (ver sección de JS):
    - Al submit del form: llamar POST /auth/login
    - Si éxito: guardar token en variable global window.AUTH_TOKEN,
      guardar rol y nombre en window.AUTH_ROL y window.AUTH_NOMBRE
      y redirigir a doctor.html o enfermero.html según el rol
    - Si error: mostrar error-msg con el mensaje del backend
    - Mostrar "Ingresando..." en el botón durante la llamada
    - Deshabilitar el botón durante la llamada

── frontend/doctor.html ────────────────────────────

Estructura:
  <title>SOLCA — Parte Diario | Dr. [nombre dinámico]</title>
  Link al css/solca.css

  <nav class="navbar">:
    Div logo: "🏥 SOLCA — Parte Diario Médico"
    Div user-info:
      Span id="nombre-medico" (se rellena con JS)
      Span id="fecha-hoy" (se rellena con JS con la fecha de hoy)
      Div con dos botones: btn-secondary "⬇ PDF" id="btn-pdf",
                           btn-secondary "⬇ Excel" id="btn-excel"
      Btn btn-secondary id="btn-logout": "Cerrar sesión"

  <div class="resumen-bar">:
    Span: "Pacientes hoy:"
    Span id="total-pacientes" clase badge-completo
    Span: "| Completos:"
    Span id="total-completos" clase badge-completo
    Span: "| Pendientes:"
    Span id="total-pendientes" clase badge-pendiente

  <div class="panel-main">:
    Div id="estado-carga": "Cargando agenda..." (se oculta cuando llegan datos)
    Div id="sin-pacientes" oculto: "No hay pacientes agendados para hoy."
    Div class="table-container":
      Table class="agenda" id="tabla-agenda":
        Thead con columnas:
          # | N° HC | Apellidos | Nombres | Edad | Sexo |
          CIE-10 | Diagnóstico | Convenio |
          Especialidad | Actividad | Tipo Consulta |
          PRE QT | PRE QX | QUIMIO | EKG | Estado
        Tbody id="tbody-agenda" (vacío, se rellena con JS)

  <script src="js/auth.js">
  <script src="js/api.js">
  <script src="js/doctor.js">

── frontend/enfermero.html ─────────────────────────

Estructura:
  <title>SOLCA — Vista Global | Enfermería</title>
  Link al css/solca.css

  <nav class="navbar">:
    Logo igual al doctor.html
    user-info: nombre del enfermero, botón PDF global, botón Concentrado Excel,
               botón logout

  <div class="filtros-bar">:
    Label + input date id="fecha-inicio"
    Label + input date id="fecha-fin"
    Label + select id="filtro-medico": opción "Todos los médicos" + opciones dinámicas
    Btn btn-primary id="btn-filtrar": "Aplicar filtros"
    Btn btn-secondary id="btn-concentrado": "⬇ Concentrado Mensual Excel"

  <div class="resumen-bar">:
    Igual que en doctor pero con todos los médicos

  <div class="panel-main">:
    Div class="table-container":
      Table class="agenda" id="tabla-global":
        Thead con las mismas columnas que la del doctor MÁS una columna
        "Médico" al inicio (antes de N° HC)
        Tbody id="tbody-global" (vacío, se rellena con JS)
        Todos los campos en modo LECTURA (sin selects ni checkboxes editables)

  <script src="js/auth.js">
  <script src="js/api.js">
  <script src="js/enfermero.js">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVOS 23–26 DE N: JavaScript del Frontend
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

── frontend/js/auth.js ─────────────────────────────

/*
 * auth.js — Manejo de autenticación y JWT en memoria.
 * El token NUNCA se guarda en localStorage ni sessionStorage.
 * Se mantiene en window._solcaAuth durante la sesión del navegador.
 */

Define el objeto window._solcaAuth = { token, rol, medicoId, nombre }

Función: solcaLogin(username, password) -> Promise
  - POST a http://localhost:8000/auth/login
  - Si éxito: guarda en window._solcaAuth y redirige
  - Si error: lanza el error para que el llamador lo muestre

Función: solcaLogout()
  - Limpia window._solcaAuth
  - Redirige a index.html

Función: solcaGetToken() -> string | null
  - Retorna el token actual o null

Función: solcaCheckAuth()
  - Si no hay token, redirige a index.html
  - Llamar esta función al inicio de doctor.js y enfermero.js

── frontend/js/api.js ──────────────────────────────

/*
 * api.js — Wrapper de Fetch con inyección automática del JWT.
 * Usar siempre apiFetch() en vez de fetch() directamente.
 */

const API_BASE = "http://localhost:8000";

Función: async apiFetch(path, options = {}) -> Response
  - Agrega header Authorization: Bearer <token> automáticamente
  - Agrega Content-Type: application/json si el body no es FormData
  - Si la respuesta es 401: llama solcaLogout() automáticamente
  - Si la respuesta no es ok: lanza error con el mensaje del backend

Función: async apiGet(path) -> data (json)
Función: async apiPut(path, body) -> data (json)
Función: async apiDownload(path, filename)
  - Hace fetch, obtiene blob, crea URL temporal, dispara descarga,
    limpia la URL. Sin abrir nueva ventana.

── frontend/js/doctor.js ───────────────────────────

/*
 * doctor.js — Lógica completa de la vista del médico.
 */

Al cargar el DOM (DOMContentLoaded):
  1. Llamar solcaCheckAuth() — redirige si no hay token
  2. Verificar que el rol sea "doctor" — si no, redirigir a index.html
  3. Mostrar nombre del médico en #nombre-medico
  4. Mostrar fecha de hoy formateada en #fecha-hoy (DD/MM/YYYY)
  5. Cargar catálogos: GET /catalogos/especialidades y almacenar en
     variable local `especialidades` (array)
     Para cada especialidad, cargar también sus actividades y almacenar
     en `actividadesPorEsp` = { [especialidadId]: [actividades] }
     Hacer TODAS estas llamadas en paralelo con Promise.all()
  6. Cargar agenda: GET /agenda/dia
  7. Renderizar la tabla con los datos recibidos
  8. Actualizar los contadores del resumen-bar

Función renderTablaDoctor(registros):
  Por cada registro crea una fila <tr> con:
  - Si registro.ComplementoCompleto: agregar clase "completa" al tr
  - Celdas de solo lectura para campos HIS
  - Celda con <select> de especialidades (id="esp-{AgendamientoId}")
    Opción vacía al inicio: "— Seleccione —"
    Poblar con los datos de `especialidades`
    Si ya hay Complemento.EspecialidadId: pre-seleccionar esa opción
  - Celda con <select> de actividades (id="act-{AgendamientoId}")
    Inicialmente deshabilitado y vacío si no hay especialidad seleccionada
    Si hay especialidad: poblar con actividades y pre-seleccionar si aplica
  - Celda con <select> de tipo consulta (id="tc-{AgendamientoId}")
    Opciones: vacía "— Seleccione —", "Primera Vez" / PRIMERA_VEZ,
              "Subsecuente" / SUBSECUENTE
    Pre-seleccionar si hay Complemento.TipoConsulta
  - 4 celdas con checkboxes centrados:
    id="qt-{AgendamientoId}", "qx-{AgendamientoId}",
    "quimio-{AgendamientoId}", "ekg-{AgendamientoId}"
    Pre-marcar si hay complemento con True
  - Celda de estado: span id="estado-{AgendamientoId}"
    "✓" verde si ComplementoCompleto, "—" gris si no

  Evento onChange en el select de Especialidad:
    - Limpiar el select de Actividad
    - Obtener las actividades de `actividadesPorEsp[nuevaEspId]`
    - Poblar el select de Actividad con esas opciones
    - Habilitar el select de Actividad
    - Disparar autoGuardar(AgendamientoId)

  Evento onChange en Actividad, TipoConsulta, y Checkboxes:
    - Disparar autoGuardar(AgendamientoId)

Función autoGuardar(agendamientoId):
  - Implementar con debounce de 500ms usando setTimeout/clearTimeout
  - Leer los valores actuales de todos los campos de esa fila
  - Validar que EspecialidadId y ActividadId no sean vacíos antes de llamar
    Si son vacíos: NO llamar a la API (no guardar incompleto)
  - Si son válidos: llamar PUT /complemento/{agendamientoId}
  - Al completarse exitosamente:
    - Mostrar el indicador guardado de esa fila (agregar clase "visible")
    - Después de 2000ms: quitar la clase "visible"
    - Actualizar la clase "completa" en el <tr> de esa fila
    - Actualizar los contadores del resumen-bar

Botón #btn-pdf: addEventListener click →
  apiDownload("/exportar/pdf", "ParteDiario_" + fechaHoy + ".pdf")

Botón #btn-excel: addEventListener click →
  apiDownload("/exportar/excel", "ParteDiario_" + fechaHoy + ".xlsx")

Botón #btn-logout: addEventListener click → solcaLogout()

── frontend/js/enfermero.js ────────────────────────

/*
 * enfermero.js — Lógica de la vista global del enfermero.
 */

Al cargar el DOM:
  1. solcaCheckAuth() y verificar rol "enfermero"
  2. Mostrar nombre del enfermero
  3. Establecer valores por defecto en los filtros de fecha:
     fecha-inicio = primer día del mes actual (YYYY-MM-01)
     fecha-fin    = hoy (YYYY-MM-DD)
  4. Cargar lista de médicos desde mock data para poblar el
     select #filtro-medico (extraer MedicoId y nombre único de la
     respuesta de /agenda/global o definir un endpoint simple
     GET /catalogos/medicos que retorne los médicos del mock)
  5. Llamar cargarVistaGlobal() con los filtros por defecto

Función cargarVistaGlobal():
  - Construir query params desde los filtros activos
  - GET /agenda/global?fecha_inicio=...&fecha_fin=...&medico_id=...
  - Renderizar tabla en modo solo lectura
  - Actualizar resumen-bar

Función renderTablaEnfermero(registros):
  - Por cada registro crea una fila <tr> de solo lectura
  - Columna Médico: muestra el MedicoId o nombre (si se provee)
  - Checkboxes: mostrar "✓" o "—" como texto, NO como inputs
  - TipoConsulta: mostrar "Primera Vez" o "Subsecuente" como texto
  - Especialidad y Actividad: mostrar el nombre (requiere lookup
    del catálogo que también debe cargarse al inicio)

Botón #btn-filtrar: addEventListener click → cargarVistaGlobal()

Botón #btn-concentrado: addEventListener click →
  Construir los mismos query params de los filtros activos y llamar:
  apiDownload("/concentrado/mensual/exportar?...",
              "Concentrado_SOLCA_" + mesActual + ".xlsx")

Botón #btn-logout: addEventListener click → solcaLogout()

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVO FINAL: README.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Genera un README.md completo con:

## Sistema de Parte Diario Médico — SOLCA v1.0.0

### Requisitos previos
  - Python 3.11 o superior
  - pip

### Instalación y arranque (primera vez)

  # 1. Clonar o descomprimir el proyecto
  cd solca-parte-diario

  # 2. Crear entorno virtual
  python -m venv .venv
  source .venv/bin/activate        # Linux/Mac
  .venv\Scripts\activate           # Windows

  # 3. Instalar dependencias
  pip install -r requirements.txt

  # 4. Aplicar migraciones (crea la BD SQLite)
  alembic upgrade head

  # 5. Cargar datos de catálogo (especialidades y actividades)
  python seed.py

  # 6. Iniciar el servidor
  uvicorn backend.main:app --reload --port 8000

  # 7. Abrir el frontend
  Abrir frontend/index.html en el navegador
  (o usar Live Server de VS Code apuntando a la carpeta frontend/)

### Usuarios de prueba
  | Usuario         | Contraseña | Rol       |
  |-----------------|------------|-----------|
  | dr.gutierrez    | Solca2026! | Doctor    |
  | dr.paredes      | Solca2026! | Doctor    |
  | enf.torres      | Solca2026! | Enfermero |

### Estructura de pacientes en el mock
  - dr.gutierrez (MedicoId=10): 3 pacientes
  - dr.paredes   (MedicoId=11): 2 pacientes
  - (MedicoId=12):              1 paciente (sin usuario de prueba)

### Endpoints disponibles
  Documentación interactiva: http://localhost:8000/api/docs

### Migrar a SQL Server (producción)
  1. Editar .env: cambiar HIS_DATA_SOURCE=mock por HIS_DATA_SOURCE=sql
  2. Completar las variables HIS_DB_SERVER, HIS_DB_NAME, etc.
  3. Instalar driver: pip install pyodbc
  4. Reiniciar el servidor

### Migrar a PostgreSQL
  1. Editar DATABASE_URL en .env
  2. Ejecutar: alembic upgrade head
  3. Ejecutar: python seed.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERIFICACIONES FINALES — ANTES DE CERRAR TU RESPUESTA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Antes de terminar, verifica mentalmente cada punto:

  [ ] Todos los archivos listados en la estructura de carpetas
      fueron generados con su ruta exacta como comentario de encabezado

  [ ] mock_data.json tiene exactamente los 6 registros especificados
      con los campos AgendamientoId y MedicoId en cada uno

  [ ] La tabla Complemento_Parte_Diario tiene AgendamientoId UNIQUE
      para garantizar el UPSERT correcto

  [ ] El endpoint PUT /complemento/{id} verifica en el backend
      que el agendamiento pertenece al médico del token (no confía
      solo en el frontend)

  [ ] Los selectores de Especialidad y Actividad están vinculados:
      cambiar especialidad limpia y recarga actividades SIN llamadas
      extra a la API (los datos ya están en memoria desde el inicio)

  [ ] El auto-save usa debounce de 500ms y NO bloquea la interfaz

  [ ] CERO modales para acciones cotidianas en toda la aplicación

  [ ] Todos los colores del frontend usan exactamente la paleta SOLCA
      definida en las variables CSS (nada de colores hardcodeados
      fuera de solca.css)

  [ ] El README tiene los 7 pasos de instalación numerados
      y la tabla de usuarios de prueba

  [ ] requirements.txt tiene versiones fijadas para todas las
      dependencias (sin rangos con ~= ni >=)

Si alguna verificación falla, corrige el archivo correspondiente
antes de terminar tu respuesta.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FIN DEL PROMPT MAESTRO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ══════════════════════════════════════════════
## FIN DEL BLOQUE A COPIAR
## ══════════════════════════════════════════════

---

## Notas de uso del Prompt Maestro

### Cómo pegarlo en Cursor

1. Abrir Cursor en la carpeta vacía donde vivirá el proyecto.
2. Abrir el panel de chat (`Ctrl+L` o `Cmd+L`).
3. Seleccionar el modelo más capaz disponible (Claude Sonnet o GPT-4o).
4. Copiar todo el contenido entre las marcas `INICIO` y `FIN` del bloque de arriba.
5. Pegar en el chat y enviar.
6. Si la respuesta se corta, escribir: **"Continúa desde donde te quedaste"** hasta que todos los archivos estén generados.

### Cómo pegarlo en Claude Code

```bash
# En la terminal, dentro de la carpeta del proyecto:
claude "$(cat 04_Prompt_Maestro_Desarrollo.md | sed -n '/INICIO DEL PROMPT/,/FIN DEL PROMPT/p')"
```

### Qué esperar como resultado

La IA generará en una sola respuesta (o en varias si la cortas) todos los archivos listados en la estructura de carpetas. Al terminar, ejecuta los 7 comandos del README en orden y el sistema estará corriendo en menos de 5 minutos.

### Prompts de seguimiento recomendados

Si algo no quedó bien, usa estos prompts de corrección quirúrgica:

**Si los colores no son los correctos:**
> "Revisa todo frontend/css/solca.css. Asegúrate de que NINGÚN color
> esté hardcodeado fuera de las variables :root. Todos los azules
> deben usar var(--azul) y todos los fondos var(--blanco)."

**Si el auto-save no funciona:**
> "Reescribe la función autoGuardar() en doctor.js. Debe usar
> setTimeout/clearTimeout para debounce de 500ms. No debe bloquear
> la interfaz. El indicador 'Guardado' debe aparecer en la celda
> de estado de la misma fila, no en una alerta global."

**Si la seguridad de roles falla:**
> "Revisa el endpoint PUT /complemento/{agendamiento_id} en
> backend/routers/complemento.py. Debe verificar que el
> agendamiento_id pertenece al medico_id extraído del JWT,
> consultando his_service. Si no pertenece: HTTPException 403."

**Si los selectores dinámicos no funcionan:**
> "Revisa doctor.js. El evento onChange del select de Especialidad
> debe: 1) limpiar el select de Actividad, 2) filtrar
> actividadesPorEsp[nuevaEspId] en memoria local (sin llamada API),
> 3) poblar el select de Actividad, 4) habilitarlo."

**Para conectar el SQL Server real:**
> "Implementa la función _obtener_desde_sql() en
> backend/services/his_service.py usando pyodbc y SQLAlchemy.
> La query SQL a usar es exactamente la del documento de requisitos.
> Agrégale el filtro AND AG.MedicoId = :medico_id al WHERE.
> Envuelve todo en try/except y lanza HTTPException 503 si falla."
```

---

*Documento elaborado por el equipo de Tech Lead. El Prompt Maestro está versionado junto al repositorio del proyecto. Actualizar cuando cambien los requisitos técnicos.*
