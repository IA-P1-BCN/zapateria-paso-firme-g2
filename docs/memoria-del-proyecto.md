# Memoria del proyecto · Zapatería Paso Firme

**Automatización de la tienda con n8n sobre una app FastAPI ya existente**

| Dato | Valor |
|---|---|
| Repositorio | `zapateria-paso-firme-g2` |
| Rama analizada | `fix/joining-workflows-essential-level` (2 commits por delante de `develop`, 0 por detrás) |
| Equipo | Levi Flores (`levifvy`), Brian Hañari (`BrianStiv`), Miguel Matesanz (`mmatesanzg23`) |
| Stack | FastAPI + SQLite + HTML/CSS/JS + n8n + Docker Compose |
| Fecha de la memoria | 29 de octubre de 2026 |
| Alcance construido | Nivel Esencial completo y parte del Nivel Medio (9 flujos exportados) |
| Estado | Flujos versionados y validados; **ninguno activo** en n8n; quedan credenciales, pruebas de extremo a extremo y PR |

> Esta memoria se ha redactado leyendo el repositorio completo en la rama `fix/joining-workflows-essential-level`: enunciado, guía de la app, ontología, constitución, specs, planes, tareas, fixtures, flujos JSON, infraestructura de agentes, ADR, CI, datos de ejemplo y código de la app. No sustituye a las specs: las resume y las conecta. Al final se compara esta rama con el resto para responder dónde está mejor desarrollado el proyecto.

---

## 1. Resumen ejecutivo

La Zapatería Paso Firme es un negocio de barrio que trabaja con **apartados**: el cliente reserva un par de zapatos dejando un abono inicial y paga el resto a plazos. La tienda ya dispone de una **aplicación web** (FastAPI + SQLite + interfaz HTML/JS) que registra apartados, abonos, ventas y vales, aplica las reglas del negocio y avisa a n8n mediante un webhook.

El proyecto **no consiste en programar esa app**, sino en construir a su alrededor un conjunto de **automatizaciones en n8n**: confirmaciones, recibos, conciliación de Bizum/transferencias, cierre de caja, control de vencimientos, informes y avisos de error. La app es la **fuente de verdad** de los importes y del estado de cada apartado; n8n solo consulta, suma, decide y comunica.

Para que el trabajo sea trazable y seguro, el equipo adopta **Spec-Driven Development (SDD)**: cada automatización nace de una historia de usuario, se escribe como spec, se aprueba por una persona, se desglosa en plan y tareas, se construye como flujo JSON y se revisa antes de la PR. Además, el repositorio incluye una **capa de agentes de IA** (subagentes, skills, comandos, validadores y bitácora) que automatiza parte del ciclo sin saltarse nunca la revisión humana.

**Resultado a la fecha:** existen 9 flujos exportados (`000`–`008`), todos con `"active": false` y validados por `scripts/validate_workflows.py --estricto` (9/9). Los flujos esenciales están construidos y, en esta rama, el enrutador ya está cableado con confirmación y recibo. Falta la puesta en marcha real en n8n: crear credenciales, sustituir los marcadores `<<ASIGNAR_EN_N8N>>`, probar con fixtures, activar y abrir las PR.

---

## 2. Contexto y problema

### 2.1 La tienda antes de automatizar

Marisa, dueña de la zapatería, gestionaba los apartados en un **Excel** (`data/excel_actual_apartados.csv`) y las ventas en otra hoja (`data/excel_actual_ventas.csv`). Ese Excel presenta los problemas típicos de una hoja manual:

- fechas en formatos distintos (`02/09/2026`, `7/9/26`);
- importes escritos a mano con símbolos y errores (`15€`, `"1.842,30"` como texto);
- nombres de cliente duplicados con mayúsculas y minúsculas (`Carmen Ruiz` / `carmen ruiz`);
- teléfonos ausentes o con espacios;
- notas en lenguaje natural (`"dijo que paga el resto el viernes"`, `"LIQUIDADO - recogió"`);
- filas que mezclan apartados, abonos y ventas.

A la vez, los pagos llegan por **Bizum o transferencia** y hay que conciliarlos a mano contra el apartado correcto; los avisos del banco se mezclan con publicidad. El cierre de caja se hace con calculadora y el control de los **90 días de plazo** depende de que alguien se acuerde.

### 2.2 El problema a resolver

Automatizar sin tocar la app:

1. avisar al cliente en el momento de apartar y en cada abono;
2. registrar solos los pagos a distancia cuando no haya duda y preguntar a Marisa cuando la haya;
3. cerrar la caja cada noche y enviar el resumen;
4. avisar de ventas grandes y de apartados próximos a vencer o vencidos;
5. enviar un informe mensual con recaudación y pendiente;
6. avisar al equipo si una automatización falla;
7. hacerlo con **cero secretos en el repositorio**, **mínimos datos personales** y **errores visibles**.

### 2.3 Restricciones de partida

- `backend/` y `frontend/` son **solo lectura**. Si falta un endpoint o un campo, se anota como `<<PENDIENTE>>` y decide una persona.
- El webhook de la app es **uno solo** y **no se autentica**; no se puede cambiar desde el proyecto.
- La app envía el aviso **una vez y sin reintentos**; por eso los flujos críticos consultan la API en lugar de depender del evento.
- No se activan flujos desde un agente: la activación es una decisión humana.

---

## 3. Objetivos y alcance

### 3.1 Objetivo general

Construir una capa de automatización en n8n, fiable y auditable, que reduzca el trabajo manual de Marisa y de la tienda sin modificar la aplicación existente.

### 3.2 Niveles de entrega

El enunciado organiza el trabajo en cuatro niveles. El equipo prioriza **Esencial** y **Medio**; Avanzado y Experto quedan documentados como visión.

| Nivel | Contenido | Flujos / HUs |
|---|---|---|
| **Esencial** | Confirmación, recibo, abonos a distancia, cierre diario, error workflow y enrutador | FL-01, FL-02, FL-03, FL-05, FL-08 |
| **Medio** | Venta grande, recordatorios/vencimientos, informe mensual, migración del Excel y sub-flujos reutilizables | FL-04, FL-06, FL-07, HU-10 |
| **Avanzado** | Asistentes de Telegram (cliente y Marisa), entrada automática de datos, datos personales | HU-11 a HU-14 |
| **Experto** | Panel de Marisa y operación continua (despliegue, backups, CI, MCP) | HU-15, HU-16 |

### 3.3 Criterios de éxito del proyecto

- Los importes que se comunican son **exactamente** los de la app.
- Ningún flujo contiene credenciales ni datos personales reales.
- Cualquier fallo deja rastro visible (Error Workflow + ejecución en n8n).
- Cada flujo tiene spec aprobada, fixtures y revisión humana antes de mergear.
- La documentación permite a otra persona reconstruir el sistema sin preguntar.

---

## 4. El dominio del negocio

El modelo conceptual está en `ontology.md`; la fuente ejecutable de las reglas es `backend/config.py` y `backend/models/`.

### 4.1 Entidades

| Entidad | Qué es | Campos relevantes |
|---|---|---|
| **Apartado** | Un par de zapatos reservado por un cliente | `id`, `fecha`, `cliente`, `telefono`, `email`, `producto`, `talla`, `precio`, `fecha_limite`, `estado` |
| **Abono** | Pago parcial de un apartado (incluye el abono inicial) | `id`, `apartado_id`, `fecha`, `importe`, `forma_pago` |
| **Vale** | Crédito generado cuando un apartado vence | `id`, `codigo` (`VALE-NNNNN`), `apartado_id`, `fecha`, `importe`, `usado` |
| **Venta** | Venta directa de mostrador, sin apartado | `id`, `fecha`, `concepto`, `importe`, `forma_pago` |

No existe una tabla de clientes ni un catálogo de productos: el cliente son campos de texto del apartado y el producto es texto libre.

### 4.2 Reglas del negocio

| Regla | Contenido |
|---|---|
| R-01 | El abono inicial mínimo es **5 €** y no puede superar el precio. |
| R-02 | El plazo es de **90 días**: `fecha_limite = fecha + 90 días`. |
| R-03 | Los abonos pueden ser de cualquier importe, pero **nunca superiores a lo pendiente**. |
| R-04 | Solo se abona si el apartado está `activo` y no ha pasado `fecha_limite`. |
| R-05 | `liquidado` lo pone la app automáticamente cuando `pendiente` llega a 0. |
| R-06 | `vencido` **no** lo pone la app sola: n8n llama a `POST /api/apartados/{id}/vencer`. |
| R-07 | Al vencer se genera un vale por el importe abonado. |
| R-08 | Formas de pago válidas: `efectivo`, `tarjeta`, `bizum`. **No existe `transferencia`.** |
| R-09 | Una venta directa no genera apartado ni vale. |
| R-10 | Un apartado fuera de plazo sigue `activo` hasta que alguien lo vence. |
| R-11 | Los importes calculados (`abonado`, `pendiente`, `estado`, `fecha_limite`, importe del vale) se usan **tal cual**. |
| R-12 | La IA puede extraer datos de un texto, pero **no decide**: decide el flujo con IF/Switch y la API. |
| R-13 | Los datos personales se limitan al mínimo imprescindible (RGPD). |

### 4.3 Ciclo de vida del apartado

```
creado (activo)
   │  abonos parciales
   ├── pendiente = 0 ──────────────▶ liquidado   (lo pone la app)
   └── hoy > fecha_limite ─────────▶ vencido     (lo pone n8n vía POST /vencer)
                                        └── genera vale por lo abonado
```

### 4.4 Métricas de Marisa

- **Ventas del día:** ventas directas + abonos del día.
- **Recaudación mensual:** ventas directas y abonos del mes, **por separado**.
- **Total pendiente de cobro:** suma de `pendiente` de los apartados `activo`.
- **Cierres e informes:** desglose por forma de pago cuando el flujo lo requiera.

### 4.5 La trampa de la transferencia

La app solo acepta `efectivo`, `tarjeta` y `bizum`. Cuando un correo del banco es una **transferencia**, el flujo `003` la registra como `bizum` y **avisa a Marisa de que el origen era una transferencia**. Es una decisión consciente, documentada en ADR-0002 (D12) y en la spec 003, pendiente de confirmar con la dueña.

---

## 5. Arquitectura del sistema

### 5.1 Vista general

```
┌──────────────────────────┐        ┌──────────────────────────┐
│  Navegador de la tienda  │        │        Gmail             │
│  HTML + CSS + JS         │        │  avisos del banco        │
└────────────┬─────────────┘        └────────────┬─────────────┘
             │ X-API-Key                         │ etiqueta "Banco"
             ▼                                   ▼
┌──────────────────────────┐        ┌──────────────────────────┐
│  App FastAPI  :8000      │        │   n8n  :5678             │
│  apartados / abonos      │◀───────│   HTTP Request + IA      │
│  ventas / vales / Excel  │  API   │   Switch / IF / Code     │
│  SQLite (tienda.db)      │        │   Gmail / Sheets / Data  │
└────────────┬─────────────┘        └────────────┬─────────────┘
             │ webhook POST /webhook/tienda      │
             └───────────────────────────────────┘
                 { evento, datos }  (una vez, sin reintentos)
```

### 5.2 Servicios Docker

`docker-compose.yml` levanta dos servicios:

| Servicio | Imagen / build | Puerto | Papel |
|---|---|---|---|
| `tienda` | build local de `backend/` | `8000` | App FastAPI + frontend + SQLite |
| `n8n` | imagen oficial de n8n | `5678` | Automatizaciones |

Detalles relevantes:

- Zona horaria `Europe/Madrid` en ambos.
- Dentro de la red de Docker, la app es `http://tienda:8000` y n8n es `http://n8n:5678`. **Desde dentro de n8n nunca se usa `localhost`.**
- Volúmenes para la base de datos de la tienda y para los datos de n8n.
- La app arranca con datos de ejemplo si la base está vacía (`SEED=1`).

### 5.3 Flujo de integración

**App → n8n (eventos):**

```
POST http://n8n:5678/webhook/tienda
Content-Type: application/json

{
  "evento": "apartado.creado | abono.registrado | venta.registrada | apartado.vencido",
  "datos": { ... }
}
```

La app lo envía en segundo plano y **no reintenta** si n8n está caído. En n8n el cuerpo llega dentro de `body`: `{{ $json.body.evento }}`, `{{ $json.body.datos.estado }}`.

**n8n → app (consultas y acciones):**

```
GET  http://tienda:8000/api/apartados?estado=activo
POST http://tienda:8000/api/apartados/{id}/abonos
POST http://tienda:8000/api/apartados/{id}/vencer
```

Siempre con la cabecera `X-API-Key`, mediante la credencial **Header Auth** `API tienda` creada en la UI. El valor nunca está en el JSON.

### 5.4 Decisiones de arquitectura

| Decisión | Motivo |
|---|---|
| Un único webhook con Switch | La app solo apunta a una URL; añadir flujos no obliga a tocar la configuración. |
| Flujos programados que consultan la API | El webhook puede perderse; los datos críticos se recalculan desde la fuente. |
| La app calcula, n8n suma y comunica | Evita duplicar reglas y discrepancias de importes. |
| Gmail como canal único | Decisión del equipo (ADR-0002, D12); evita fragmentar canales y credenciales. |
| Google Sheets solo donde aporta histórico | Cierres y almacenes anti-duplicados; el resto se envía por correo. |
| JSON con `"active": false` | Regla dura: un agente nunca activa flujos. |
| Configuración con nodo Set, no con `$vars` | `$vars` requiere licencia de n8n; en la instancia local llega vacío (comprobado el 2026-10-29). |

---

## 6. La aplicación existente

### 6.1 Estructura MVC

```
backend/
  main.py            junta las piezas y monta routers
  config.py          entorno (.env) + reglas del negocio
  database.py        SQLite, consultas y creación de tablas
  models/            datos y reglas (apartado, abono, venta, vale, errores)
  schemas/           Pydantic: forma de entrada y salida
  routes/            URL → controlador
  controllers/       lógica de cada petición
  middleware/        X-API-Key y traducción de errores a HTTP
  services/n8n.py    envío del webhook
  seed.py            datos de ejemplo realistas
  tests/             pytest de la API y del seed
frontend/            HTML, CSS y JS sin framework
```

La interfaz **no tiene lógica de negocio**: pide los datos a la misma API que usa n8n y envía la cabecera `X-API-Key` (la recibe en `/config.js`, una decisión explícita para una app sin login).

### 6.2 Endpoints

| Método | Ruta | Para qué |
|---|---|---|
| `GET` | `/api/apartados` | Lista con filtros `estado`, `q`, paginación y `X-Total-Count` |
| `GET` | `/api/apartados/resumen` | Conteo por estado |
| `GET` | `/api/apartados/{id}` | Detalle con `abonos[]` y `vale` |
| `POST` | `/api/apartados` | Crear apartado con abono inicial |
| `POST` | `/api/apartados/{id}/abonos` | Registrar abono |
| `POST` | `/api/apartados/{id}/vencer` | Vencer y generar vale |
| `GET` | `/api/abonos?desde=&hasta=` | Abonos entre fechas (incluidas) |
| `GET` | `/api/ventas?desde=&hasta=&orden=` | Ventas entre fechas |
| `POST` | `/api/ventas` | Registrar venta directa |
| `GET` | `/api/vales` | Vales generados |
| `GET` | `/api/excel` | Descargar todos los datos en `.xlsx` |
| `GET` | `/` , `/apartados/nuevo`, `/apartados/{id}`, `/ventas` | Páginas HTML |
| `GET` | `/config.js` | Clave de API para el navegador |

### 6.3 Seguridad y errores

- Todas las rutas `/api/...` exigen `X-API-Key`; sin ella o con valor incorrecto devuelven **401**.
- `404` si el recurso no existe.
- `422` si se rompe una regla de negocio (`{"detail": "..."}`).
- El webhook de salida **no lleva autenticación**: es un bloqueo conocido que exigiría tocar el backend.

### 6.4 Lo que la app no tiene (y condiciona el diseño)

| Carencia | Consecuencia |
|---|---|
| Forma de pago `transferencia` | El flujo 003 registra como `bizum` y avisa del origen. |
| Endpoint para marcar un vale como usado | El vale se genera, pero su uso se gestiona fuera de la app. |
| Registro de consentimiento y de avisos enviados | n8n usa Data Tables propias. |
| Fecha exacta de liquidación | El informe 008 la aproxima por el último abono. |
| Autenticación del webhook | HU-14 queda bloqueada; el enrutador no puede verificar origen. |
| Login de usuarios | La clave de API viaja al navegador; solo apto para red local. |

---

## 7. Metodología: Spec-Driven Development

### 7.1 El ciclo

```
HU del enunciado
  → /sdd-spec        → spec.md (Borrador)
  → revisión humana  → Estado: Aprobada
  → /sdd-plan        → plan.md
  → /sdd-tasks       → tasks.md
  → /construir-flujo → workflows/NNN-slug.json
  → /revisar-flujo   → revisión de seguridad + contrato de API
  → PR + revisión humana
  → /bitacora        → docs/ai-log.md
```

Nada se construye sin spec aprobada. Una tarea del Kanban = un flujo (o parte) = una rama = una PR.

### 7.2 La constitución

`specs/constitution.md` fija diez principios no negociables:

| # | Principio | Implicación práctica |
|---|---|---|
| I | La app calcula, n8n no recalcula importes | `abonado`, `pendiente`, `estado`, `fecha_limite` se usan tal cual |
| II | La IA extrae, el flujo decide | IF/Switch/Code y la API deciden; nunca el modelo |
| III | Cero secretos en el repositorio | Credenciales solo en la UI de n8n |
| IV | No se toca la app | `backend/` y `frontend/` son solo lectura |
| V | Un único webhook | La app no se reconfigura por cada flujo |
| VI | Los flujos se exportan desactivados | `"active": false` |
| VII | Sin cambios en la app sin decisión humana | `<<PENDIENTE>>` y ADR |
| VIII | Los fallos se ven | Error Workflow asignado |
| IX | Mínimos datos personales | Solo lo imprescindible, sin IA cuando no hace falta |
| X | Los flujos críticos consultan la API | No dependen del aviso del webhook |

### 7.3 Convenciones (ADR-0002)

- Nombre de flujo: `[NNN] Nombre en español`, con el número de la **spec** (no el `FL-XX` del enunciado).
- Sub-flujos: `[SUB] …`; Error Workflow: `[ERR] …`; enrutador: `[000] …`.
- Nodos: verbo + objeto (`Pedir apartado a la API`, `Enviar recibo al cliente`); IF/Switch como pregunta (`¿Liquidado?`).
- Archivo: `workflows/NNN-slug.json`, tres dígitos.
- Rama: `feature/HU-XX-slug`.
- Variables configurables (umbral, hora, correo) en variables de n8n, no incrustadas en el nodo.
- Redondeo: solo los **totales** a 2 decimales; los sumandos se usan tal cual.
- Gmail como canal único; Data Tables para idempotencia.

### 7.4 La capa de agentes

El repositorio incorpora una infraestructura para trabajar con IA de forma reproducible:

| Pieza | Contenido |
|---|---|
| `.agents/agents/` | Subagentes: `spec-writer`, `flow-builder`, `flow-reviewer`, `api-contract-checker`, `test-designer`, `ai-scribe` |
| `.agents/commands/` | `/sdd-spec`, `/sdd-plan`, `/sdd-tasks`, `/construir-flujo`, `/revisar-flujo`, `/bitacora` |
| `.claude/skills/` | Fuente única de skills (proyecto + equipo + externas adaptadas) |
| `.opencode/` | Configuración de OpenCode; agentes, comandos y skills **generados** |
| `.agents/decisions/` | ADR-0001 (infraestructura) y ADR-0002 (convenciones de flujos) |
| `scripts/` | `sync_agents.py`, `validate_agent_infra.py`, `validate_workflows.py`, `new_feature.py`, `gemini_review.py` |

Los subagentes **no se llaman entre sí**: el agente principal orquesta y cada paso tiene revisión humana. Las skills se editan solo en `.claude/skills/` y se copian a `.opencode/skills/` con `python scripts/sync_agents.py`.

### 7.5 Validaciones automáticas

| Comando | Qué comprueba |
|---|---|
| `python scripts/validate_workflows.py workflows --estricto` | JSON válido, nodos completos, sin credenciales, `active: false`, nombre `NNN-slug.json` |
| `python scripts/validate_agent_infra.py` | Skills, cabeceras SCOPE, sincronización, specs y terminología |
| `python scripts/validate_agent_infra.py --alcance --base develop` | Además, que la rama no toque código de la app |
| `cd backend && pytest` | Que la app sigue funcionando (no se modifican tests) |

**Evidencia de la última ejecución en esta rama (29/10/2026):**

- `validate_workflows.py --estricto`: **9/9 flujos válidos**.
- `validate_agent_infra.py`: **8 problemas** (falta cabecera SCOPE en 006 y 007, falta `spec.md` en 007) y **129 marcadores `<<PENDIENTE>>`**.
- `pytest` no pudo ejecutarse en el entorno local de esta revisión porque el intérprete usado no tiene `pytest` instalado. No se instala ni se modifica nada: la verificación queda pendiente en el entorno del equipo o en CI.

---

## 8. Equipo y forma de trabajo

### 8.1 Personas y reparto

Equipo de tres personas; cada feature la hace **una persona entera** (spec, flujo, pruebas, PR) y la revisa **otra** que no la construyó.

| Feature | Hace | Revisa |
|---|---|---|
| 000 Enrutador | Miguel | Levi |
| 001 Confirmación | Brian | Miguel |
| 002 Recibo | Miguel (cierre) | Levi |
| 003 Abonos a distancia | Levi | Brian |
| 004 Cierre diario | Miguel | Brian |
| 005 Error Workflow | Brian | Levi |
| 006 Venta grande | Levi | Brian |
| 007 Recordatorios | Brian | Miguel |
| 008 Informe mensual | Miguel | Levi |

### 8.2 Ceremonias y tablero

- **Daily Scrum** de lunes a viernes, 15 min, referencia 09:00 `Europe/Madrid`.
- Una tarjeta por equipo y día (`[Daily] AAAA-MM-DD`), creada automáticamente por `.github/workflows/daily-scrum.yml` (cron `30 6 * * 1-5`).
- Facilitador rotatorio: Levi → Brian → Miguel (ancla 2026-10-26).
- Un único Project con vistas `tablero`, `por historia`, `se puede empezar`, `Dailies` e `Historial de dailys`.
- Los bloqueos detectados se convierten en issues con etiqueta `bloqueado` y responsable.

### 8.3 Reglas de colaboración

- Una feature = una rama = una PR; nadie edita el JSON de una feature ajena.
- El enrutador `000` es compartido: cambios en PR aparte y avisando.
- Commits en español, en imperativo, los hace una persona (no el agente).
- PR a `develop` con al menos una aprobación.
- Cambios en `.agents/`, `.claude/`, `.opencode/`, `scripts/` o la constitución van en PR propia.

---

## 9. Catálogo de automatizaciones

### 9.1 Mapa feature ↔ flujo ↔ estado

| Feature | HU | FL | Nivel | Spec | Flujo | Estado real en esta rama |
|---|---|---|---|---|---|---|
| 000 Enrutador de eventos | requisito esencial | — | Esencial | Aprobada | Sí | **Cableado con 001 y 002**; Error Workflow pendiente en UI |
| 001 Confirmación de apartado | HU-01 | FL-01 | Esencial | Aprobada | Sí | Ajustado (email trim, remitente, sin atribución); credencial pendiente |
| 002 Recibo de abono | HU-02 | FL-02 | Esencial | Aprobada | Sí | Construido; credencial y pruebas pendientes |
| 003 Abonos a distancia | HU-03 | FL-03 | Esencial | Aprobada | Sí | Construido; pendiente prueba integral y decisión sobre transferencias |
| 004 Cierre diario | HU-04 | FL-05 | Esencial | Aprobada | Sí | Ajustado sin `$vars`; pendiente credenciales y prueba |
| 005 Avisos de error | HU-05 | FL-08 | Esencial | Aprobada | Sí | Construido; asignación en cada flujo pendiente |
| 006 Venta grande | HU-09 | FL-04 | Medio | **Borrador** | Sí | Construido con desviaciones; sin aprobar |
| 007 Recordatorios y vencimientos | HU-06, HU-07 | FL-06 | Medio | **No existe** | Sí | Construido con desviaciones; plan/tasks sin spec |
| 008 Informe mensual | HU-08 | FL-07 | Medio | Aprobada | Sí | Construido; Error Workflow pendiente de asignar en UI |
| 009 Migración del Excel | HU-10 | — | Medio | No | No | Sin empezar |

> El `specs/backlog.md` está desactualizado: marca 000–005 como Borrador o “En construcción” cuando sus specs ya están Aprobadas y sus flujos construidos. La tabla de arriba refleja el contenido real de `specs/features/`.

### 9.2 [000] Enrutador de eventos

- **Objetivo:** un único webhook que reparte los eventos con un Switch.
- **Disparador:** `POST /webhook/tienda` (responde al recibir).
- **Ramas:** `apartado.creado` → Code `Extraer datos del apartado` → `[001]`; `abono.registrado` → Code `Extraer datos del abono` → `[002]`; `venta.registrada` y `apartado.vencido` → No Op hasta que existan 006/007 con Execute Workflow Trigger; evento desconocido → rama de descarte.
- **Detalle técnico:** los Code nodes ponen `body.datos` en la **raíz** del item, porque los sub-flujos 001 y 002 esperan el apartado plano desde su Execute Workflow Trigger. Sin ese desempaquetado, los campos llegarían anidados y las expresiones `$json.cliente` fallarían.
- **Estado:** 10 nodos; `settings.errorWorkflow = <<ASIGNAR_EN_N8N>>`; los `workflowId` de los Execute Workflow también son marcadores.
- **Pendiente:** enlazar los ids reales de 001, 002 y `[ERR]` en la UI, y probar de extremo a extremo creando un apartado y un abono desde la app (T-000-08 sigue abierta).

### 9.3 [001] Confirmación de apartado

- **Objetivo:** el cliente recibe al momento el resumen de lo apartado.
- **Disparador:** `apartado.creado` desde 000.
- **Salida:** email al cliente con nº de apartado, producto, talla, precio, abonado, pendiente y fecha límite; si no hay email, aviso a la tienda.
- **Reglas:** importes de la app tal cual; formato español (`79,90 €`); `talla` nula se omite; si nace `liquidado`, se dice que ya puede recogerlo.
- **Ajustes de esta rama:** el IF usa `String($json.email ?? '').trim()` para tratar cadenas vacías o con espacios; el envío usa `$json.email.trim()`; se añade `senderName: "Zapatería Paso Firme"` y `appendAttribution: false`; `correo_tienda` pasa a `tienda@pasofirme.example`, alineado con el `tienda_email` de 002.
- **Datos personales:** nombre y email solo hacia Gmail; el teléfono no se usa.
- **Pendiente:** credencial `Gmail tienda` y buzón real de la tienda.

### 9.4 [002] Recibo de abono

- **Objetivo:** recibo tras cada abono y aviso de recogida al liquidar.
- **Disparador:** `abono.registrado` desde 000 (también cuando el abono lo crea 003).
- **Decisión de diseño:** el evento no trae `forma_pago` ni id del abono; el recibo no los muestra y el flujo no llama a la API.
- **Salidas:** recibo, aviso de recogida o aviso a la tienda si falta email.
- **Textos:** cerrados en la spec, con importes y fechas en formato español.
- **Observación:** la spec menciona la credencial `Correo tienda`, mientras el resto del proyecto usa `Gmail tienda`. Conviene unificar el nombre antes de la puesta en marcha.

### 9.5 [003] Abonos a distancia (Bizum / transferencia)

Es el flujo más complejo (24 nodos) y el que más valor aporta.

- **Disparador:** Gmail Trigger sobre la etiqueta `Banco`.
- **Extracción:** Gemini (capa gratuita) devuelve JSON con `es_pago`, `tipo`, `ordenante`, `importe`, `concepto` y `referencia_apartado`.
- **Decisión:** el flujo —no la IA— comprueba:
  - remitente contra `BANCO_REMITENTES`;
  - que sea un pago;
  - un único apartado claro por nombre y/o referencia;
  - importe ≤ pendiente;
  - apartado `activo` y dentro de plazo;
  - que la referencia aparezca literalmente en el correo (anti-alucinación).
- **Acción:** `POST /api/apartados/{id}/abonos` con `forma_pago: "bizum"`; si era transferencia, además avisa a Marisa.
- **Dudas:** no registra nada y pregunta a Marisa por Gmail con candidatos y motivo.
- **Idempotencia:** Data Table `Emails` por `message_id`; se anota `en_proceso` **antes** de registrar y se actualiza al final. Si falla a mitad, queda `en_proceso` y avisa: se prefiere un pago sin registrar a un abono duplicado.
- **RGPD:** solo se envía al modelo el asunto y el cuerpo del aviso del banco; nunca la lista de apartados ni datos de clientes.
- **Pruebas:** los 9 correos de `data/correos/` (Bizum, transferencias y publicidad).

### 9.6 [004] Cierre diario

- **Disparador:** Schedule Trigger a las 21:30 `Europe/Madrid`.
- **Entradas:** ventas y abonos del día (`desde=hoy`, `hasta=hoy`).
- **Cálculo:** totales por forma de pago (`efectivo`, `tarjeta`, `bizum`) y total general; solo los totales se redondean a 2 decimales.
- **Salidas:** fila en Google Sheets, hoja `Cierres`, con upsert por `fecha`; email a Marisa.
- **Bordes:** día sin movimientos → mensaje “Hoy no hubo movimientos”, no error; una forma sin movimientos → `0,00 €`.
- **Ajuste de esta rama:** se añade un nodo `Configuración` con `MARISA_EMAIL` y `GOOGLE_SHEETS_CIERRES_ID`, y se sustituyen las referencias a `$vars` por `$('Configuración').first().json.*`. Motivo: sin licencia de n8n, `$vars` llega vacío (comprobado el 2026-10-29). El flujo pasa de 7 a 8 nodos.

### 9.7 [005] Avisos de error (Error Workflow)

- **Disparador:** Error Trigger cuando falla un flujo que lo tiene asignado.
- **Salida:** email a la tienda con flujo, nodo, mensaje enmascarado, fecha/hora y enlace a la ejecución.
- **Enmascarado:** `X-API-Key`, `Authorization`, `Bearer …`, `password`, `apiKey` y datos personales de clientes.
- **Decisión:** no se agrupan errores y no se reintenta el flujo; n8n no encadena Error Workflows, así que un fallo del propio aviso solo queda en *Executions*.
- **Observación:** el JSON del Error Workflow no se asigna a sí mismo (correcto). Los demás flujos todavía llevan `<<ASIGNAR_EN_N8N>>` porque los ids cambian en cada instancia.

### 9.8 [006] Venta grande

- **Objetivo:** avisar a Marisa cuando una venta supera un umbral configurable.
- **Disparador previsto:** Schedule cada 15 min **o** webhook `venta.registrada`.
- **Salida:** email a Marisa + registro en Data Table `avisos_ventas_grandes`.
- **Estado:** spec en **Borrador**; preguntas abiertas sobre umbral, canal y disparador.
- **Desviaciones detectadas al leer spec y JSON:**
  - la spec pide `cliente`, `producto`, `talla` y `email` de la venta, pero `VentaOut` solo tiene `concepto`, `importe`, `forma_pago` y `fecha`;
  - el JSON usa nodos `emailSend` y `n8nDataTable` en lugar de los nodos Gmail/Data Table convenidos;
  - no tiene `settings.errorWorkflow`;
  - incluye un Error Trigger dentro del propio flujo, lo que no sustituye la asignación del Error Workflow.

  Antes de aprobar la spec hay que corregir el contrato de datos o limitar el aviso a los campos que existen.

### 9.9 [007] Recordatorios y vencimientos

- **Objetivo:** cada mañana a las 06:00 avisar de pagos pendientes y vencer los apartados fuera de plazo.
- **Estado:** **no existe `spec.md`**; solo plan, tareas y fixtures. No debería construirse ni mergearse sin spec aprobada.
- **Desviaciones detectadas:**
  - el plan llama “vencimiento” a `pendiente == 0`, cuando un apartado con pendiente 0 ya está `liquidado`; el vencimiento es `hoy > fecha_limite` con pendiente > 0;
  - la llamada `GET /api/apartados?estado=activo&fecha_limite=...` usa un parámetro que la API **no acepta**; hay que filtrar en n8n;
  - el JSON usa `n8nDataTable` y `emailSend`, y no lleva `settings.errorWorkflow`;
  - no hay endpoint para marcar el vale como usado, así que el aviso de vale es solo informativo.
- **Conclusión:** el flujo existe, pero la especificación debe reescribirse antes de considerarlo entregable.

### 9.10 [008] Informe mensual

- **Disparador:** día 1 de cada mes a las 08:00 `Europe/Madrid`.
- **Entradas:** ventas y abonos del mes anterior, apartados activos, todos los apartados, vales y detalle de cada liquidado.
- **Cálculo:** recaudación separada (ventas directas / abonos / total), pendiente total, conteos de nuevos, liquidados y vencidos.
- **Aproximación documentada:** la app no guarda fecha de liquidación; se usa el último abono.
- **Bordes:** mes sin datos → informe con ceros; listas vacías → “Always Output Data”; 404/422 en el detalle → aviso y continuar.
- **Salida:** email HTML a Marisa; sin histórico en Sheets (fuera de alcance).
- **Observación:** en esta rama el `settings.errorWorkflow` vuelve a `<<ASIGNAR_EN_N8N>>` (antes tenía el nombre literal), porque los ids de workflow no son portables entre instancias.

---

## 10. Inventario de flujos exportados

| Archivo | Nombre en n8n | Nodos | Disparador | `errorWorkflow` |
|---|---|---|---|---|
| `000-enrutador-eventos.json` | `[000] Enrutador de eventos` | 10 | Webhook | `<<ASIGNAR_EN_N8N>>` |
| `001-confirmacion-apartado.json` | `[001] Confirmación de apartado` | 7 | Execute Workflow | `<<ASIGNAR_EN_N8N>>` |
| `002-recibo-abono.json` | `[002] Recibo de abono` | 9 | Execute Workflow | `<<ASIGNAR_EN_N8N>>` |
| `003-abonos-a-distancia.json` | `[003] Abonos a distancia` | 24 | Gmail Trigger | `<<ASIGNAR_EN_N8N>>` |
| `004-cierre-diario.json` | `[004] Cierre diario` | 8 | Schedule | `<<ASIGNAR_EN_N8N>>` |
| `005-error-workflow.json` | `[ERR] Avisos de error` | 4 | Error Trigger | — |
| `006-venta-grande.json` | `[006] Aviso de ventas grandes` | 9 | Schedule + Webhook + Error | — |
| `007-recordatorios-vencimientos.json` | `[007] Recordatorios y Vencimientos` | 12 | Schedule + Error | — |
| `008-informe-mensual.json` | `[008] Informe mensual` | 12 | Schedule | `<<ASIGNAR_EN_N8N>>` |

**Lectura del inventario:**

- Los 9 JSON son válidos y están desactivados.
- 001, 002, 003, 004 y 008 llevan el marcador `<<ASIGNAR_EN_N8N>>`: hay que abrir cada flujo en n8n y elegir `[ERR] Avisos de error` en *Settings → Error Workflow*. No se puede dejar el nombre literal porque el id cambia entre instancias.
- 000 también lleva el marcador en su propio Error Workflow y en los dos Execute Workflow; además hay que enlazar los ids de 001 y 002.
- 005 no se asigna a sí mismo (correcto).
- 006 y 007 no tienen Error Workflow y se desvían de las convenciones de nodos y de contrato de datos; son los que requieren más trabajo antes de una PR.
- El número de nodos no indica calidad: 003 es el más complejo y el que más casos de borde documenta; 004 y 008 son los más maduros en configuración y manejo de errores.

---

## 11. Datos de prueba

### 11.1 Datos de ejemplo de la app

`backend/seed.py` genera una base realista con `random.Random(42)` para que sea reproducible:

- 24 apartados con escenarios calculados respecto a **hoy**:
  - 83 días → vence en 7 días;
  - 89 días → vence mañana;
  - 96, 104 y 118 días → fuera de plazo, aún `activo`;
  - 12–88 días → algunos ya `liquidado`;
  - 130 días → `vencido` con vale;
  - 0 y 1 días → recién creados.
- Abonos parciales y liquidaciones.
- Ventas directas de los últimos 75 días, sin domingos.
- Nombres, productos y formas de pago variados.

Los tests `test_datos_de_ejemplo.py` comprueban que hay apartados que vencen en 7 y 1 días, fuera de plazo, liquidados, vales y ventas de hoy; además verifican clientes concretos que aparecen en los correos.

### 11.2 Correos del banco

`data/correos/` contiene **9 `.eml`**:

| Archivo | Caso |
|---|---|
| `01_bizum_carmen.eml` | Bizum claro de Carmen |
| `02_bizum_jorge.eml` | Bizum claro de Jorge |
| `03_transferencia_lucia.eml` | Transferencia de Lucía |
| `04_bizum_laura.eml` | Bizum de Laura |
| `05_bizum_romero.eml` | Bizum con nombre abreviado |
| `06_bizum_paula.eml` | Bizum de Paula |
| `07_transferencia_desconocido.eml` | Transferencia de desconocido |
| `08_publicidad_banco.eml` | Publicidad: debe ignorarse |
| `09_bizum_silvia.eml` | Bizum de Silvia |

Los fixtures de 003 documentan el resultado esperado de cada uno: registrar, no registrar o preguntar. El briefing habla de “8 correos”, pero la carpeta, su tabla y el PRD tienen 9; la spec lo deja anotado.

### 11.3 Fixtures por feature

Cada feature incluye `fixtures.md` con payloads de webhook, respuestas de API y casos de borde. Los más completos son 003 (9 correos y matriz de decisión) y 008 (meses con y sin datos, errores 401/404/422). 006 y 007 tienen fixtures mínimos, coherente con su estado de madurez.

### 11.4 Estrategia de prueba

1. Importar el JSON en un n8n local.
2. Crear las credenciales en la UI (nunca en el JSON).
3. Ejecutar con la *Test URL* y los payloads de `fixtures.md`.
4. Comprobar la app (apartados, abonos, vales) y los correos.
5. Repetir el mismo evento para verificar idempotencia.
6. Probar errores: clave incorrecta (401), id inexistente (404), importe excesivo (422).
7. Solo después, una persona decide activar.

---

## 12. Trazabilidad de la IA

`docs/ai-log.md` registra las sesiones de trabajo con modelo, prompts clave, resultados, errores y decisiones. No es un adorno: documenta fallos reales y cómo se corrigieron.

### 12.1 Entradas registradas

| Fecha | Trabajo | Aprendizaje principal |
|---|---|---|
| 2026-10-23 | Infraestructura de agentes, skills y SDD | La capa de agentes necesita validadores y sincronización para no divergir |
| 2026-10-26 | HU-02 / 002 · Recibo de abono | Un flujo sencillo obliga a decidir qué datos no trae el evento |
| 2026-10-29 | HU-03 / 003 · Puesta en marcha y anomalías | La IA puede inventar identificadores y duplicar flujos; hay que verificar contra n8n |
| 2026-10-29 | HU-05 / 005 · Error Workflow y revisión MCP | El enmascarado de secretos y datos personales es parte del diseño, no un extra |
| 2026-10-29 | HU-03 / T-003-07 · Prueba con los 9 correos | Los casos dudosos son más importantes que el camino feliz |
| 2026-10-27 | 000 / T-000-07 · Enrutador | El contrato `body.evento` es la fuente de errores más común |
| 2026-10-29 | 004 / T-004-08 · Cierre diario | Los totales se redondean; los sumandos no; `$vars` no existe sin licencia |

### 12.2 Errores y alucinaciones documentados

- **IDs de flujo inventados** al referenciar flujos en n8n: se corrigió verificando contra la instancia real.
- **Flujos duplicados** tras importar varias veces: se limpió y se fijó el procedimiento de importación.
- **Correos en spam** al enviar desde Gmail: se ajustó la configuración y se documentó.
- **Bug de enmascarado de JWT** en el Error Workflow: el mensaje podía filtrar el token; se corrigió antes de dar por válido el flujo.
- **Riesgo de `docker compose down -v`**: borra volúmenes y datos; se advierte en la documentación.
- **Parámetros de API inventados** en planes (por ejemplo `fecha_limite` en la lista de apartados): el validador de contrato y la lectura de `backend/routes/` los detectan.
- **`$vars` vacío sin licencia**: detectado al probar 004; se sustituyó por un nodo `Configuración` con Set.

### 12.3 Decisiones aceptadas o rechazadas

| Decisión | Estado |
|---|---|
| Gmail como canal único | Aceptada (ADR-0002, D12) |
| Transferencias registradas como `bizum` con aviso | Aceptada, pendiente de confirmar con Marisa |
| Data Table `Emails` para idempotencia | Aceptada |
| Form Trigger solo en flujo `[TEST]` no exportado | Aceptada |
| Gemini en capa gratuita para extracción | Aceptada con riesgo RGPD documentado |
| Google Sheets para cierres | Aceptada |
| Responder a Marisa por el mismo correo del banco | Rechazada |
| Activar flujos desde un agente | Rechazada |
| Nodo Set `Configuración` en lugar de `$vars` | Aceptada tras comprobar que `$vars` llega vacío |

---

## 13. Calidad, seguridad y RGPD

### 13.1 Controles implantados

- **Sin secretos:** el validador busca `apiKey`, `token`, `password`, `sk-…` y claves de Google; las credenciales se referencian por nombre.
- **Sin datos personales reales:** los fixtures usan nombres y correos de ejemplo; el seed genera datos ficticios.
- **Mínimo dato al modelo:** 003 solo envía asunto y cuerpo del aviso del banco.
- **Enmascarado en errores:** 005 elimina claves y datos de clientes del mensaje.
- **Salida desactivada:** todos los JSON tienen `"active": false`.
- **Validación en CI:** pytest + validadores en cada PR (`.github/workflows/ci.yml`).
- **Plantilla de PR:** obliga a declarar flujo, spec, pruebas, secretos y datos personales.

### 13.2 Riesgos abiertos

| Riesgo | Impacto | Mitigación actual | Qué falta |
|---|---|---|---|
| Webhook sin autenticación | Cualquiera en la red puede inyectar eventos | Red local; no se toca el backend | Decisión humana (HU-14) |
| Clave de API en el navegador | Cualquiera con acceso a la app puede leerla | Apto solo para red local | Login real si se publica |
| Gemini capa gratuita | Google puede usar el contenido para mejorar sus productos | Solo se envía el aviso del banco | Confirmar modelo y política con la tienda |
| Sin endpoint para usar vales | El vale no se descuenta en la app | Aviso informativo | Decisión de negocio |
| Sin fecha de liquidación | El informe 008 aproxima | Último abono | Añadir campo a la app (requiere decisión) |
| Sin consentimiento de recordatorios | Riesgo RGPD si se envían SMS/email | Solo transaccionales | Definir base legal y almacén |
| 129 `<<PENDIENTE>>` | Bloquean la puesta en marcha | Documentados | Resolverlos con el equipo |
| Marcadores `<<ASIGNAR_EN_N8N>>` | Los flujos no quedan conectados al importar | Notas en cada flujo | Enlazar ids en la UI y probar |

### 13.3 Deuda técnica y de documentación

- `specs/backlog.md` no refleja el estado real de las specs.
- 006 está en Borrador y su contrato de datos no encaja con `VentaOut`.
- 007 no tiene spec y su plan confunde vencimiento con liquidación.
- 006 y 007 no siguen las convenciones de nodos ni llevan Error Workflow.
- La credencial de 002 se llama `Correo tienda` en la spec y `Gmail tienda` en el resto.
- Falta evidencia de pytest en esta revisión; la CI lo cubre cuando se ejecute.
- El nombre de la carpeta `zapateria-paso-firme-g2` y el remitente del banco son datos de ejemplo: no deben tratarse como reales.

---

## 14. Dónde está mejor desarrollado el proyecto

### 14.1 Comparación de ramas

Se compararon todas las ramas locales y remotas contra `develop`:

| Rama | Delante | Detrás | Lectura |
|---|---:|---:|---|
| `fix/joining-workflows-essential-level` | **2** | **0** | **La más avanzada y actualizada**: integra 000 con 001/002 y corrige 004/001 |
| `develop` | 0 | 0 | Base con 003, 004, 005, 006, 007 y 008 ya mergeados |
| `origin/feature/HU-08-informe-mensual` | 0 | 3 | Ya mergeada; no aporta nada nuevo |
| `origin/feature/HU-04-cierre-diario` | 0 | 19 | Ya mergeada; superada por esta rama |
| `origin/feature/HU-05-avisos-errores` | 0 | 25 | Ya mergeada |
| `origin/flujo/venta-grande` | 0 | 5 | Ya mergeada; 006 sigue en Borrador |
| `origin/flujo/recordatorios-vencimientos` | 0 | 16 | Ya mergeada; 007 sigue sin spec |
| `origin/fix/000-cableado-errorworkflow` | 1 | 4 | Versión anterior del cableado; superada por esta rama |
| `feature/HU-03-abonos-a-distancia` (local) | 1 | 12 | Tiene un fix de 003 **sin mergear** (`3ef5b77`), pero está sobre un `develop` antiguo |
| `main` | 0 | 61 | Muy atrás; no es la línea de trabajo |

### 14.2 Veredicto

**El proyecto está mejor desarrollado en `fix/joining-workflows-essential-level`.** Es la única rama que:

- está por delante de `develop` sin estar por detrás;
- tiene el enrutador `000` realmente cableado con `001` y `002` (Execute Workflow + desempaquetado de `body.datos`);
- corrige la configuración de `004` para que funcione sin licencia de pago (`$vars` → nodo Set);
- pule `001` (email con `trim`, remitente y sin atribución de n8n);
- mantiene los 9 flujos y las specs de 000–008 (salvo 007).

### 14.3 Matices por área

| Área | Dónde está mejor | Comentario |
|---|---|---|
| **Backend / dominio** | `backend/` de `develop` (idéntico en todas las ramas) | Es la parte más madura del repositorio: reglas, endpoints, tests y seed. No se toca. |
| **Enrutador 000** | Esta rama | 10 nodos, dos ramas cableadas, Error Workflow preparado. |
| **Confirmación 001** | Esta rama | Ajustes de email y dirección de ejemplo. |
| **Recibo 002** | Esta rama / `develop` | 9 nodos; solo falta credencial y prueba. |
| **Abonos a distancia 003** | `feature/HU-03-abonos-a-distancia` (local) | Tiene el fix `3ef5b77` que separa errores técnicos de la API; **no está mergeado** y su base es antigua. Hay que rebasar o cherry-pick, no mergear tal cual (borraría 006/007/008). |
| **Cierre diario 004** | Esta rama | Configuración sin `$vars`; 8 nodos. |
| **Error Workflow 005** | `develop` / esta rama | 4 nodos, enmascarado y Gmail; falta asignarlo en todos los flujos. |
| **Venta grande 006** | `develop` | Existe, pero spec Borrador y contrato de datos incorrecto. |
| **Recordatorios 007** | `develop` | Existe, pero sin spec y con errores conceptuales. |
| **Informe mensual 008** | `develop` / esta rama | 12 nodos; solo falta asignar Error Workflow en UI. |
| **Documentación y SDD** | Esta rama | Specs, planes, fixtures, PRD, diagramas, ADR y bitácora; la más completa. |
| **Frontend** | `frontend/` de `develop` | Funcional pero mínimo; no es el foco del proyecto. |

### 14.4 Qué haría falta para que esta rama sea la definitiva

1. Enlazar en n8n los ids de `001`, `002` y `[ERR]` en `000`, y el Error Workflow en 001–004 y 008.
2. Probar de extremo a extremo: crear apartado → confirmación; abono → recibo; los 9 correos → 003; cierre → 004; error provocado → 005.
3. Recuperar el fix de 003 (`3ef5b77`) con rebase/cherry-pick, sin arrastrar la eliminación de 006/007/008.
4. Reescribir la spec 007 y corregir 006 antes de considerarlas entregables.
5. Actualizar `specs/backlog.md` y abrir la PR con la plantilla.

---

## 15. Hoja de ruta

### 15.1 Cierre del nivel Esencial

1. Crear en n8n las credenciales `API tienda` (Header Auth) y `Gmail tienda` (OAuth2).
2. Sustituir `<<ASIGNAR_EN_N8N>>` por `[ERR] Avisos de error` en 000, 001, 002, 003, 004 y 008.
3. Enlazar en 000 los workflows `[001]` y `[002]`.
4. Ejecutar los fixtures de 001, 002, 003, 004 y 005.
5. Verificar los 9 correos del banco y la idempotencia por `message_id`.
6. Abrir las PR con la plantilla y revisión cruzada.

### 15.2 Cierre del nivel Medio

1. Reescribir la spec 007 con el criterio correcto de vencimiento y sin parámetros inexistentes.
2. Corregir el contrato de datos de 006 o reducir su alcance a `concepto`/`importe`.
3. Aprobar 006 y 007, y actualizar `specs/backlog.md`.
4. Probar 008 con un mes sin datos y con datos.
5. Implementar 009 (migración del Excel) con los CSV reales.
6. Crear los sub-flujos `[SUB]` 010 y 011 si se confirma su necesidad.

### 15.3 Nivel Avanzado y Experto

- Asistentes de Telegram para clientes y Marisa.
- Entrada automática de datos desde datáfono o correo.
- Política transversal de datos personales y consentimiento.
- Panel de Marisa y operación continua (backups, CI, MCP).

---

## 16. Conclusiones

El proyecto demuestra que se puede automatizar una zapatería real **sin reescribir su aplicación** y sin poner en riesgo sus datos. La clave no ha sido la herramienta, sino el método:

1. **La app manda.** Los importes y estados se leen, no se recalculan. Esto elimina la clase de error más peligrosa en un negocio de cobros.
2. **Un solo webhook y flujos que consultan.** El sistema tolera que se pierda un aviso porque los procesos críticos se recalculan desde la API.
3. **La IA extrae, el flujo decide.** El modelo ayuda a leer un correo del banco, pero nunca registra un pago por su cuenta.
4. **Todo se documenta y se valida.** Specs, fixtures, ADR, validadores, CI y bitácora permiten que otra persona entienda y revise el trabajo.
5. **Nada se activa solo.** Los JSON viajan desactivados y la puesta en marcha es una decisión humana.

El estado actual es el de un sistema **construido y verificable, pero no implantado**: los flujos existen y validan, las specs esenciales están aprobadas, el enrutador ya está cableado y los datos de prueba cubren los casos difíciles; faltan credenciales, pruebas integrales en n8n, corrección de 006/007 y las PR. La rama `fix/joining-workflows-essential-level` es, hoy, la foto más avanzada y coherente del proyecto.

---

## Anexos

### A. Mapa de archivos

| Ruta | Contenido |
|---|---|
| `docs/BRIEFING_zapateria.md` | Enunciado, HUs y niveles |
| `docs/guia-de-la-app.md` | API, webhook, errores y ejemplos |
| `docs/prd-nivel-medio.md` | PRD aprobado (Esencial + Medio) |
| `docs/prd-completo.md` | Visión completa (todos los niveles) |
| `docs/ai-log.md` | Bitácora de IA |
| `docs/dailies/README.md` | Rutina de daily y tablero |
| `docs/diagramas/` | Diagramas de flujo y automatización |
| `ontology.md` | Entidades, reglas y métricas |
| `specs/constitution.md` | Principios no negociables |
| `specs/backlog.md` | Feature ↔ HU ↔ FL ↔ estado |
| `specs/features/NNN-*/` | `spec.md`, `plan.md`, `tasks.md`, `fixtures.md` |
| `workflows/` | JSON exportados de n8n |
| `.agents/` | Subagentes, comandos y ADR |
| `.claude/skills/` | Fuente única de skills |
| `scripts/` | Sincronización y validación |
| `backend/` | App FastAPI (solo lectura) |
| `frontend/` | Interfaz (solo lectura) |
| `data/` | CSV del Excel y correos del banco |

### B. Eventos del webhook

| Evento | Cuándo | `datos` |
|---|---|---|
| `apartado.creado` | Al crear un apartado | Apartado completo con `abonado` y `pendiente` |
| `abono.registrado` | Al registrar un abono | Apartado actualizado + `importe` del abono |
| `venta.registrada` | Al registrar una venta | Venta |
| `apartado.vencido` | Al vencer un apartado | `{ apartado, vale }` |

### C. Glosario

| Término | Significado |
|---|---|
| **Apartado** | Reserva de un par de zapatos con abono inicial y plazo |
| **Abono** | Pago parcial; el inicial cuenta como abono |
| **Liquidado** | Apartado con pendiente 0; lo marca la app |
| **Vencido** | Apartado fuera de plazo; lo marca n8n y genera vale |
| **Vale** | Crédito por lo abonado en un apartado vencido |
| **Cierre** | Resumen diario de caja por forma de pago |
| **Recaudación** | Ventas directas + abonos, separados |
| **Pendiente de cobro** | Suma de `pendiente` de los activos |
| **Spec** | Documento que define objetivo, reglas, bordes y criterios |
| **Fixture** | Payload o caso de prueba reproducible |
| **Error Workflow** | Flujo que recibe los fallos de otros flujos |

### D. Convenciones de nombres

- Flujo: `[NNN] Nombre` / `[SUB] Nombre` / `[ERR] Nombre`.
- Archivo: `NNN-slug.json`.
- Nodo: verbo + objeto; decisión como pregunta.
- Rama: `feature/HU-XX-slug`.
- Spec: `specs/features/NNN-slug/`.

---

*Memoria redactada a partir de la lectura completa del repositorio en la rama `fix/joining-workflows-essential-level`. Las cifras de estado y los resultados de validación corresponden al 29/10/2026 y deben actualizarse cuando se cierren las tareas pendientes.*
