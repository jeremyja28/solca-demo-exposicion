# 01 — Requisitos y Casos de Uso
## Sistema de Parte Diario Médico — SOLCA

> **Versión:** 1.0  
> **Fecha:** Junio 2026  
> **Estado:** Borrador para revisión  
> **Clasificación:** Documento interno — uso restringido

---

## 1. Contexto y Objetivo

### 1.1 Problema actual

El área médica de SOLCA gestiona diariamente el registro de atenciones a través de hojas de cálculo Excel elaboradas manualmente. Este proceso presenta las siguientes deficiencias:

- Duplicación de datos ya existentes en el sistema hospitalario (HIS).
- Riesgo de errores de transcripción en nombres, diagnósticos CIE-10 y datos demográficos del paciente.
- Imposibilidad de consolidar información de múltiples doctores sin intervención manual.
- Ausencia de trazabilidad, auditoría y control de versiones.
- Generación de reportes mensuales lenta y propensa a inconsistencias.

### 1.2 Objetivo del sistema

Digitalizar el proceso de generación del **Parte Diario Médico** mediante una aplicación web que:

- Precargue automáticamente los datos de pacientes agendados desde las vistas del sistema hospitalario (HIS/SOLCA).
- Permita al médico completar únicamente los campos que no existen en el HIS.
- Ofrezca al personal de enfermería una vista global consolidada con capacidad de filtrado y exportación.
- Elimine la dependencia del Excel manual sin interrumpir el flujo clínico.

### 1.3 Fuente de datos

Los datos de pacientes se obtienen mediante la consulta SQL existente sobre las vistas del HIS de SOLCA, que provee los siguientes campos precargados:

| Campo HIS | Descripción |
|-----------|-------------|
| `N_HC` | Número de historia clínica (identificación) |
| `APELLIDOS` | Primer y segundo apellido |
| `NOMBRES` | Nombres del paciente |
| `FECHA_NACIMIENTO` | Fecha de nacimiento |
| `EDAD` | Edad calculada en años |
| `SEXO` | Sexo del paciente |
| `CIE10` | Código(s) de diagnóstico CIE-10 |
| `DIAGNOSTICO` | Descripción del diagnóstico |
| `PROCEDENCIA` | Dirección / procedencia del paciente |
| `CONVENIO` | Nombre del convenio o seguro médico |

---

## 2. Alcance del Sistema

### 2.1 Dentro del alcance

- Autenticación de usuarios con dos roles diferenciados.
- Visualización de agenda diaria por médico, precargada desde el HIS.
- Formulario de captura de campos complementarios por el médico.
- Vista global de todas las agendas para el personal de enfermería.
- Filtros por fecha y por médico.
- Exportación individual en PDF y Excel (por médico).
- Generación de Concentrado Mensual consolidado con sumatorias.

### 2.2 Fuera del alcance (v1.0)

- Modificación de datos clínicos provenientes del HIS.
- Gestión de citas o agendamiento de pacientes.
- Integración bidireccional de escritura hacia el HIS.
- Aplicación móvil nativa.

---

## 3. Roles y Perfiles de Usuario

### 3.1 Doctor (Médico Especialista)

**Descripción:** Profesional médico que atiende pacientes agendados en SOLCA. Accede al sistema para revisar su agenda del día y completar los campos del parte diario correspondientes a su consulta.

**Permisos:**
- Ver únicamente los pacientes de su propia agenda del día en curso.
- Editar los campos complementarios de cada paciente.
- Exportar su parte diario personal en PDF y Excel.
- No puede ver agendas de otros médicos.
- No puede modificar datos precargados del HIS.

---

### 3.2 Enfermero/a (Personal de Enfermería / Coordinación)

**Descripción:** Personal administrativo o de enfermería con visión transversal del servicio. Responsable de consolidar la información de todos los médicos y generar los reportes institucionales.

**Permisos:**
- Ver la agenda de todos los médicos activos.
- Filtrar por rango de fechas y por médico específico.
- Generar y exportar el Concentrado Mensual.
- Exportar reportes individuales de cualquier médico.
- No puede editar los campos complementarios del parte diario de ningún médico.

---

## 4. Requisitos Funcionales

### 4.1 Módulo de Autenticación (RF-01)

- RF-01.1: El sistema debe proveer un formulario de inicio de sesión con campos de usuario y contraseña.
- RF-01.2: Al autenticarse, el sistema debe redirigir al usuario a la vista correspondiente a su rol (Doctor → agenda propia; Enfermero → vista global).
- RF-01.3: La sesión debe expirar automáticamente tras un período de inactividad configurable.
- RF-01.4: El sistema debe registrar la fecha, hora y usuario de cada inicio de sesión.

### 4.2 Módulo de Vista del Doctor (RF-02)

- RF-02.1: Al iniciar sesión, el médico debe ver únicamente los pacientes de su agenda del día en curso, ordenados cronológicamente por hora de atención.
- RF-02.2: Los datos precargados del HIS deben mostrarse en modo de sólo lectura: N° HC, Apellidos, Nombres, Fecha de Nacimiento, Edad, Sexo, CIE-10, Diagnóstico, Procedencia y Convenio.
- RF-02.3: El médico debe poder completar los siguientes campos complementarios para cada paciente:
  - **Especialidad** (selector desplegable): Al seleccionar una especialidad, el campo **Actividad** debe actualizarse dinámicamente mostrando solo las actividades correspondientes a esa especialidad.
  - **Tipo de Consulta** (selector): opciones fijas — `Primera Vez` / `Subsecuente`.
  - **PRE QT** (casilla de verificación): Indica que el paciente fue valorado para pre-quimioterapia.
  - **PRE QX** (casilla de verificación): Indica que el paciente fue valorado para pre-quirúrgico.
  - **QUIMIO** (casilla de verificación): Indica que el paciente recibió quimioterapia.
  - **EKG** (casilla de verificación): Indica que se realizó electrocardiograma.
- RF-02.4: El sistema debe guardar automáticamente el progreso del formulario (auto-guardado) sin requerir acción explícita del médico.
- RF-02.5: El médico debe poder exportar su parte diario completo del día en curso en formato PDF y en formato Excel (.xlsx).

### 4.3 Módulo de Vista Global del Enfermero (RF-03)

- RF-03.1: El enfermero debe ver en pantalla la lista consolidada de todos los médicos activos del día.
- RF-03.2: Debe poder seleccionar uno o múltiples médicos para visualizar sus respectivas agendas.
- RF-03.3: Debe poder filtrar la vista por rango de fechas (fecha inicio — fecha fin).
- RF-03.4: La vista debe mostrar el estado de completitud de cada parte diario (porcentaje de pacientes con campos complementarios completos).
- RF-03.5: El enfermero debe poder generar el **Concentrado Mensual**: reporte unificado que incluye todos los registros del período seleccionado, con filas por paciente y columnas de sumatorias al pie (total de primeras veces, subsecuentes, PRE QT, PRE QX, QUIMIO, EKG, agrupado por médico y por especialidad).
- RF-03.6: El Concentrado Mensual debe poder exportarse en formato Excel (.xlsx).

### 4.4 Módulo de Exportación (RF-04)

- RF-04.1: La exportación PDF del parte diario del médico debe contener: encabezado institucional SOLCA, nombre del médico, fecha, y tabla de pacientes con todos los campos (precargados y complementarios).
- RF-04.2: La exportación Excel del parte diario debe replicar la estructura del parte manual previo para facilitar la transición.
- RF-04.3: El Concentrado Mensual en Excel debe incluir: hoja de detalle (fila por paciente) y hoja de sumario (totales por médico y por especialidad).

---

## 5. Requisitos No Funcionales

### 5.1 Interfaz y Experiencia de Usuario (RNF-01)

- RNF-01.1: La interfaz debe ser limpia, minimalista y libre de elementos visuales innecesarios que interrumpan el flujo de trabajo clínico.
- RNF-01.2: No debe haber bloqueos, ventanas emergentes (modales) de confirmación ni interrupciones durante la captura de datos.
- RNF-01.3: La paleta de colores corporativa de SOLCA debe aplicarse en toda la interfaz: **blanco** (`#FFFFFF`) como color de fondo principal y **azul oscuro** (`#003366` o equivalente corporativo) para encabezados, botones primarios, bordes de tabla y elementos de navegación.
- RNF-01.4: La tipografía debe ser legible en pantallas de escritorio estándar (mínimo 14px para datos de tabla).
- RNF-01.5: El sistema debe ser responsivo y funcionar correctamente en resoluciones de 1280×720 en adelante.
- RNF-01.6: El tiempo de carga de la agenda diaria no debe superar los 3 segundos bajo condiciones normales de red hospitalaria.

### 5.2 Seguridad (RNF-02)

- RNF-02.1: Las contraseñas deben almacenarse con hash seguro (bcrypt o equivalente).
- RNF-02.2: La comunicación entre cliente y servidor debe realizarse sobre HTTPS.
- RNF-02.3: El acceso a los datos de un médico desde la sesión de otro médico debe estar bloqueado a nivel de backend, no solo de interfaz.

### 5.3 Integración (RNF-03)

- RNF-03.1: La carga de datos del HIS debe realizarse mediante ejecución de la consulta SQL parametrizada (por médico y fecha), sin duplicar datos en una base paralela.
- RNF-03.2: Los campos complementarios deben almacenarse en una base de datos propia del sistema, vinculada al ID de agendamiento del HIS.

---

## 6. Casos de Uso

---

### CU-01: Iniciar Sesión

**Actor:** Doctor / Enfermero  
**Precondición:** El usuario tiene credenciales válidas en el sistema.

**Flujo principal:**
1. El usuario accede a la URL del sistema.
2. El sistema muestra el formulario de inicio de sesión con campos Usuario y Contraseña.
3. El usuario ingresa sus credenciales y pulsa "Ingresar".
4. El sistema valida las credenciales contra el directorio de usuarios.
5. El sistema identifica el rol del usuario.
6. Si el rol es Doctor, redirige a la Vista de Agenda del Día (CU-02).
7. Si el rol es Enfermero, redirige a la Vista Global (CU-04).

**Flujo alternativo — credenciales inválidas:**
- En el paso 4, si las credenciales no coinciden, el sistema muestra un mensaje de error genérico ("Usuario o contraseña incorrectos") sin especificar cuál campo falló.
- El usuario puede reintentar hasta 5 veces antes de que la cuenta se bloquee temporalmente por 15 minutos.

---

### CU-02: Visualizar Agenda del Día (Doctor)

**Actor:** Doctor  
**Precondición:** El médico ha iniciado sesión correctamente.

**Flujo principal:**
1. El sistema consulta el HIS con el ID del médico autenticado y la fecha actual.
2. El sistema muestra la tabla de pacientes agendados, ordenada por hora de atención ascendente.
3. Cada fila muestra los campos precargados del HIS en modo lectura.
4. Cada fila incluye los campos complementarios vacíos o con valores previamente guardados.
5. El médico puede editar los campos complementarios directamente en la tabla (edición en línea) o expandiendo un panel lateral por paciente.
6. Los cambios se guardan automáticamente al salir del campo (evento `onBlur`).

**Flujo alternativo — sin pacientes agendados:**
- En el paso 2, si no existen pacientes para el día en curso, el sistema muestra el mensaje: "No hay pacientes agendados para hoy."

---

### CU-03: Completar Campos Complementarios (Doctor)

**Actor:** Doctor  
**Precondición:** El médico visualiza su agenda del día (CU-02).

**Flujo principal:**
1. El médico selecciona o hace clic en la fila del paciente que desea completar.
2. El sistema habilita los campos complementarios editables para esa fila.
3. El médico selecciona una **Especialidad** del menú desplegable.
4. El sistema actualiza dinámicamente el menú de **Actividad** mostrando únicamente las actividades asociadas a la especialidad seleccionada.
5. El médico selecciona la **Actividad** correspondiente.
6. El médico selecciona el **Tipo de Consulta**: `Primera Vez` o `Subsecuente`.
7. El médico marca una o más casillas de verificación según aplique: `PRE QT`, `PRE QX`, `QUIMIO`, `EKG`.
8. El sistema guarda automáticamente los valores al cambiar de campo.
9. La fila se marca visualmente como "completa" (ícono de verificación o cambio de color sutil).

**Flujo alternativo — cambio de especialidad después de seleccionar actividad:**
- En el paso 3, si el médico cambia la especialidad luego de haber seleccionado una actividad, el campo Actividad se limpia y muestra las nuevas opciones correspondientes a la especialidad recién elegida.

---

### CU-04: Exportar Parte Diario (Doctor)

**Actor:** Doctor  
**Precondición:** El médico tiene al menos un registro del día en curso.

**Flujo principal:**
1. El médico hace clic en el botón "Exportar" en su vista de agenda.
2. El sistema muestra dos opciones: `Descargar PDF` y `Descargar Excel`.
3. El médico selecciona el formato deseado.
4. El sistema genera el archivo con todos los pacientes del día (campos precargados + complementarios) y lo descarga en el navegador.
5. El archivo generado lleva el nombre: `ParteDisario_[Apellido_Doctor]_[YYYYMMDD].[pdf|xlsx]`.

---

### CU-05: Visualizar Vista Global (Enfermero)

**Actor:** Enfermero  
**Precondición:** El enfermero ha iniciado sesión correctamente.

**Flujo principal:**
1. El sistema muestra un panel con la lista de todos los médicos activos del día en curso.
2. Para cada médico, se muestra: nombre, especialidad principal, número de pacientes agendados y porcentaje de completitud del parte diario.
3. El enfermero puede hacer clic en cualquier médico para ver el detalle de su agenda.
4. El sistema muestra la agenda del médico seleccionado con todos los campos (precargados y complementarios) en modo solo lectura.

---

### CU-06: Filtrar por Fecha y Médico (Enfermero)

**Actor:** Enfermero  
**Precondición:** El enfermero se encuentra en la Vista Global (CU-05).

**Flujo principal:**
1. El enfermero selecciona un rango de fechas mediante el selector de fecha de inicio y fecha de fin.
2. El enfermero selecciona uno o más médicos del filtro de médicos (selector múltiple o lista de casillas).
3. El enfermero pulsa "Aplicar filtros".
4. El sistema actualiza la vista mostrando únicamente los registros que correspondan al rango de fechas y médicos seleccionados.
5. El número de resultados se muestra al pie del filtro.

**Flujo alternativo — sin resultados:**
- Si no existen registros para los filtros aplicados, el sistema muestra el mensaje: "No se encontraron registros para los criterios seleccionados."

---

### CU-07: Generar Concentrado Mensual (Enfermero)

**Actor:** Enfermero  
**Precondición:** El enfermero ha aplicado filtros de fecha y médico (CU-06) o se encuentra en la Vista Global.

**Flujo principal:**
1. El enfermero selecciona el mes y año del período a consolidar, o aplica el rango de fechas deseado.
2. El enfermero pulsa el botón "Generar Concentrado Mensual".
3. El sistema agrupa todos los registros del período por médico y por especialidad.
4. El sistema calcula las sumatorias: total de pacientes, primera vez, subsecuente, PRE QT, PRE QX, QUIMIO, EKG — desglosadas por médico y con totales generales.
5. El sistema presenta una previsualización del concentrado en pantalla.
6. El enfermero puede exportar el concentrado en formato Excel (.xlsx).
7. El archivo descargado contiene: Hoja 1 (`Detalle`) con una fila por paciente, y Hoja 2 (`Resumen`) con las sumatorias por médico y por especialidad.
8. El archivo se denomina: `Concentrado_Mensual_SOLCA_[YYYYMM].xlsx`.

---

## 7. Catálogo de Especialidades y Actividades

> **Nota para el equipo de desarrollo:** la relación Especialidad → Actividad debe ser configurable desde un panel de administración, sin necesidad de cambios de código. La siguiente tabla es el catálogo inicial propuesto, sujeto a validación con el área médica de SOLCA.

| Especialidad | Actividades disponibles |
|---|---|
| Oncología Médica | Consulta nueva, Consulta subsecuente, Valoración pre-QT, Valoración pre-QX, Control QT |
| Oncología Quirúrgica | Consulta nueva, Consulta subsecuente, Valoración pre-QX, Seguimiento post-quirúrgico |
| Radioterapia | Consulta nueva, Planificación, Seguimiento de tratamiento |
| Hematología | Consulta nueva, Consulta subsecuente, Control de tratamiento |
| Medicina Interna | Consulta nueva, Consulta subsecuente, Interconsulta |
| Cardiología | Consulta nueva, EKG, Ecocardiograma, Valoración pre-QT |
| *(Agregar según catálogo SOLCA)* | *(Agregar según catálogo SOLCA)* |

---

## 8. Modelo de Datos Complementario

Los siguientes campos deben persistirse en la base de datos propia del sistema, vinculados al ID de agendamiento del HIS (`AG.Id`):

| Campo | Tipo | Descripción |
|---|---|---|
| `agendamiento_id` | INTEGER (FK) | ID proveniente de `AgendamientoSolcaT.Id` |
| `medico_id` | INTEGER (FK) | ID del médico autenticado |
| `fecha_registro` | DATE | Fecha del parte diario |
| `especialidad_id` | INTEGER (FK) | ID de la especialidad seleccionada |
| `actividad_id` | INTEGER (FK) | ID de la actividad seleccionada |
| `tipo_consulta` | ENUM | `PRIMERA_VEZ` / `SUBSECUENTE` |
| `pre_qt` | BOOLEAN | Casilla PRE QT |
| `pre_qx` | BOOLEAN | Casilla PRE QX |
| `quimio` | BOOLEAN | Casilla QUIMIO |
| `ekg` | BOOLEAN | Casilla EKG |
| `creado_en` | DATETIME | Timestamp de creación |
| `actualizado_en` | DATETIME | Timestamp de última modificación |
| `creado_por` | INTEGER (FK) | ID del usuario que creó el registro |

---

## 9. Lineamientos de Diseño de Interfaz

### 9.1 Principios generales

- **Claridad por encima de densidad:** cada pantalla debe mostrar únicamente la información necesaria para la tarea en curso.
- **Cero interrupciones:** no se usarán cuadros de diálogo de confirmación para acciones cotidianas (guardar, cambiar de fila, aplicar filtros). Solo se pedirá confirmación en acciones destructivas como eliminar registros.
- **Feedback inmediato:** el guardado automático debe confirmarse con un indicador visual discreto (punto verde o texto "Guardado" por 2 segundos), sin bloquear la interacción.

### 9.2 Paleta de colores corporativa

| Elemento | Color |
|---|---|
| Fondo principal | Blanco `#FFFFFF` |
| Encabezado / Navbar | Azul oscuro SOLCA `#003366` |
| Botones primarios | Azul oscuro `#003366` con texto blanco |
| Botones secundarios | Borde azul oscuro, fondo blanco |
| Texto principal | Gris oscuro `#2C2C2C` |
| Filas de tabla (alternas) | Gris muy claro `#F5F7FA` |
| Fila con datos completos | Indicador verde discreto `#27AE60` |
| Alertas de error | Rojo `#C0392B` |
| Borde de tabla | Gris claro `#D0D7DE` |

### 9.3 Componentes clave

- **Tabla de agenda:** edición en línea, sin modales. Los campos editables se activan al hacer clic en la celda.
- **Selector de Especialidad/Actividad:** dropdowns nativos estilizados; la carga de actividades debe ser instantánea (datos precargados en cliente, no consulta al servidor).
- **Casillas de verificación:** checkboxes grandes (mínimo 20×20px) con etiqueta visible, fáciles de marcar con mouse o trackpad.
- **Barra de exportación:** botones PDF y Excel siempre visibles en la parte superior derecha de la vista del médico, sin necesidad de desplazarse.

---

## 10. Criterios de Aceptación

| ID | Criterio | Rol |
|---|---|---|
| CA-01 | El médico ve solo sus pacientes del día al iniciar sesión | Doctor |
| CA-02 | Los datos del HIS se muestran en modo lectura, sin posibilidad de edición | Doctor / Enfermero |
| CA-03 | Al cambiar la Especialidad, las Actividades se actualizan sin recargar la página | Doctor |
| CA-04 | Los cambios en campos complementarios se guardan sin pulsar un botón de guardar | Doctor |
| CA-05 | El PDF exportado incluye encabezado SOLCA y todos los campos del parte | Doctor |
| CA-06 | El enfermero puede ver las agendas de todos los médicos del día | Enfermero |
| CA-07 | El filtro por rango de fechas y médico actualiza la vista correctamente | Enfermero |
| CA-08 | El Concentrado Mensual en Excel contiene hoja de detalle y hoja de resumen con sumatorias | Enfermero |
| CA-09 | Un médico no puede acceder a la agenda de otro médico, ni siquiera modificando la URL | Doctor |
| CA-10 | La interfaz no muestra ventanas emergentes ni bloqueos durante la captura normal de datos | Doctor / Enfermero |

---

## 11. Glosario

| Término | Definición |
|---|---|
| **HIS** | Hospital Information System. Sistema hospitalario de SOLCA del que provienen los datos de pacientes y agendas. |
| **Parte Diario** | Documento que registra la actividad médica diaria de un doctor: pacientes atendidos, tipo de consulta y procedimientos realizados. |
| **Concentrado Mensual** | Reporte consolidado de todos los partes diarios de un período, con sumatorias por médico y especialidad. |
| **PRE QT** | Pre-quimioterapia. Valoración médica previa al inicio de un ciclo de quimioterapia. |
| **PRE QX** | Pre-quirúrgico. Valoración médica previa a un procedimiento quirúrgico. |
| **QUIMIO** | Registro de sesión de quimioterapia aplicada durante la consulta. |
| **EKG** | Electrocardiograma. Procedimiento de diagnóstico cardíaco. |
| **CIE-10** | Clasificación Internacional de Enfermedades, décima revisión. Estándar de codificación de diagnósticos. |
| **Primera Vez** | Consulta inicial del paciente con el médico para un episodio de atención determinado. |
| **Subsecuente** | Consulta de seguimiento, posterior a una primera vez. |

---

*Documento elaborado por el equipo de Arquitectura de Software. Para consultas o modificaciones, contactar al líder técnico del proyecto.*
