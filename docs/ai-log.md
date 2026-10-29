# Bitácora de IA

## 2026-10-23 · infraestructura de agentes · — · Capa de agentes, skills y SDD

- **Persona responsable:** levifvy
- **Herramienta y modelo:** Claude Code · Claude Opus 5.5 (`claude-opus-5-5`)
- **Subagente / comando:** agente principal (sin subagente); esta entrada, `ai-scribe`
- **Rama / Spec / PR:** `feature/HU-agentic-work` · decisiones en `.agents/decisions/ADR-0001-infraestructura-agentes.md` · PR #<<PENDIENTE>>

### Prompt clave

> <<PENDIENTE: los prompts exactos de la sesión original no están disponibles; completar por el equipo (resumidos, sin datos personales ni claves)>>

### Resultado

- `AGENTS.md` como punto de entrada común, `CLAUDE.md` que lo importa (`@AGENTS.md`) y `ontology.md`.
- `.agents/` como fuente única: 6 subagentes (`spec-writer`, `flow-builder`, `flow-reviewer`, `api-contract-checker`, `test-designer`, `ai-scribe`), 6 comandos (`/sdd-spec`, `/sdd-plan`, `/sdd-tasks`, `/construir-flujo`, `/revisar-flujo`, `/bitacora`), plantillas (`ai-log-entry.md`, `pr-checklist.md`), `team.md` y ADR-0001.
- Scripts en Python: `scripts/sync_agents.py` (genera `.claude/agents|commands` y `.opencode/agents|commands`), `scripts/validate_agent_infra.py` (resultado comunicado por el agente principal: OK, 203 marcadores `<<PENDIENTE>>`) y `scripts/new_feature.py`.
- 8 skills compartidas en `.claude/skills/`: `sdd-workflow`, `dominio-apartados`, `tienda-api`, `n8n-convenciones`, `n8n-import-export`, `revision-seguridad-flujos`, `datos-de-prueba`, `trazabilidad-ia`.
- `.claude/settings.json` con permisos (bloquea `backend/`, `frontend/` y `.env`; pide confirmación en `automation/`, commit y push) y `.opencode/opencode.jsonc`.
- `specs/`: `constitution.md`, `README.md`, plantillas, `backlog.md` y features 000–005 (spec, plan, tasks, fixtures), todas en estado **Borrador**.

### Errores o alucinaciones

No se registraron alucinaciones en esta sesión con evidencia en los archivos. <<PENDIENTE: completar por el equipo si se detectó alguna durante la sesión>>

Discrepancias detectadas entre el prompt inicial y el repositorio (no son alucinaciones del agente, pero se corrigieron):

| Qué hizo mal | Cómo se detectó | Cómo se corrigió |
|---|---|---|
| El prompt decía que el frontend es React | Revisando `frontend/`: es HTML/CSS/JS plano | Se documenta como HTML/JS plano; no se tocó el frontend |
| El prompt situaba los flujos en `automation/`; el enunciado pide `workflows/` | Comparando con `docs/BRIEFING_zapateria.md`; no existe ninguna de las dos carpetas | `automation/` provisional con `<<PENDIENTE>>` en todas partes; no se crea ninguna |

### Decisiones

| Propuesta del agente | Decisión (aceptada / rechazada / modificada) | Por qué |
|---|---|---|
| D1 · `AGENTS.md` como fuente de reglas; `CLAUDE.md` solo lo importa | <<PENDIENTE: ADR-0001 en estado Propuesta>> | Un único sitio que mantener |
| D2 · Skills en `.claude/skills/` (no en `.agents/skills/`) | <<PENDIENTE>> | Es la ruta que leen Claude Code y OpenCode |
| D3 · Cuerpo de subagentes/comandos en `.agents/`, metadatos en `sync_agents.py`, copias generadas | <<PENDIENTE>> | El frontmatter de Claude Code y OpenCode es distinto |
| D4 · Línea `# SCOPE` dentro del frontmatter YAML | <<PENDIENTE>> | El frontmatter debe empezar en la línea 1 |
| D5 · `.claude/settings.json` sin línea `# SCOPE` | <<PENDIENTE>> | JSON no admite comentarios; `opencode.jsonc` sí la lleva |
| D6 · Scripts en Python sin dependencias | <<PENDIENTE>> | El equipo trabaja en Windows y el proyecto ya usa Python |
| D7 · Sin `.mcp.json` en la raíz; n8n-mcp en ámbito local y desactivado en `opencode.jsonc` | <<PENDIENTE>> | Solo 3 archivos permitidos en la raíz y ninguna clave llega al repo |
| D8 · Nombre de flujo con el número de su spec (`[004] Cierre diario`) | <<PENDIENTE>> | Un solo número para spec, archivo y flujo |
| Specs 000–005 en `Borrador` | Aceptada (regla dura) | Ningún agente puede aprobarlas; lo hace el equipo |
| `docs/ai-log.md` no se crea durante la sesión | Aceptada | `docs/` no estaba en las rutas permitidas; lo crea `ai-scribe` en su primer uso (esta entrada) |

**Bloqueos conocidos registrados** (de `specs/backlog.md`, necesitan decisión humana):

| Tema | Afecta a | Por qué |
|---|---|---|
| La app no admite forma de pago `transferencia` | 003 | `FORMAS_PAGO = efectivo, tarjeta, bizum` en `backend/config.py` |
| El webhook se envía sin cabecera de autenticación | 000, 015 | `backend/services/n8n.py` solo manda `Content-Type`; protegerlo exigiría tocar el backend |
| No hay endpoint para marcar un vale como usado | 007 | La tabla `vales` tiene `usado`, pero no hay ruta |
| No hay registro de consentimiento ni de recordatorios enviados | 007, 015 | La app no los guarda; habrá que guardarlos en n8n / Google Sheets |
| Carpeta de flujos: `automation/` o `workflows/` | todas | El enunciado pide `workflows/` |

### Siguientes pasos

- Aprobación humana de las specs 000–005 (tareas T-000-01, T-001-01, T-002-01, T-003-01, T-004-01, T-005-01).
- Aprobar o modificar ADR-0001 y resolver los bloqueos conocidos.

## 2026-10-26 · HU-02 · #11 · Recibo de abono (spec 002 → flujo → PR)

- **Persona responsable:** levifvy
- **Herramienta y modelo:** Claude Code · Claude Opus 5.5 (`claude-opus-5-5`) como agente principal orquestador
- **Subagente / comando:** `test-designer` (fixtures) → `flow-builder` (JSON) → `flow-reviewer` + `api-contract-checker` en paralelo (revisión) → `ai-scribe` (esta entrada, T-002-07). No se usó n8n-mcp.
- **Rama / Spec / PR:** `feature/HU-02-recibo-abono` · `specs/features/002-recibo-abono/` · issue #11 (subissues #30–#36) · [PR #68](https://github.com/IA-P1-BCN/zapateria-paso-firme-g2/pull/68) («Relacionado con #11») · commits `60462f0` (docs: spec aprobada, plan, tasks, fixtures) y `bb68012` (feat: `workflows/002-recibo-abono.json`)

### Prompt clave

> Prompt de orquestación por fases 0–7: auditoría de solo lectura → aprobación humana de la spec → fixtures → JSON → prueba humana → revisión automática → PR → bitácora. Fuentes de verdad ordenadas (constitución > spec > plan > tareas > prompt), archivos permitidos explícitos, paradas obligatorias entre fases y autorización puntual de commit/push/PR como excepción a la regla 4 de `AGENTS.md` (sin merge ni force push).

### Resultado

- Spec 002 de **Borrador** a **Aprobada** (aprueba levifvy, 2026-10-26) con un diff propuesto por el agente y aceptado; plan alineado con ese diff.
- Fixtures F-002-1…F-002-12: un caso por CA y por borde (2 sintéticos para CA-3).
- Flujo `[002] Recibo de abono`: Execute Workflow Trigger → `Configuración` → `Formatear importes y fechas` → `¿Tiene correo?` → `¿Liquidado?` → 3 envíos Gmail. `active: false`, sin pinData ni credenciales, Retry On Fail con 2 intentos.
- `validate_workflows.py --estricto` OK. Prueba humana en n8n local: CA-1…CA-4 OK con fixtures. `flow-reviewer`: APROBADO (0 bloqueantes). `api-contract-checker`: CONTRATO OK. CI de la PR en verde (pytest, validar flujos, título, Gemini review sin problemas).
- Resultado global: **aceptado con cambios** (spec ampliada antes de construir).

### Errores o alucinaciones

| Qué hizo mal | Causa raíz | Cómo se detectó | Cómo se corrigió |
|---|---|---|---|
| `flow-builder` (1.er intento) convirtió el `'\n'` de la expresión del aviso a la tienda en un salto de línea real y rompió la expresión | Escapado al escribir el JSON: doble nivel (JSON + expresión JS) | El propio `flow-builder` al evaluar las expresiones contra las fixtures | Corregido el escapado y revalidado |
| Contradicción de alcance: `AGENTS.md`, `CLAUDE.md`, constitución y specs llevan `# SCOPE: … NO tocar … workflows`, pero la tarea exigía escribir en `workflows/` | Cabecera heredada de la rama de infraestructura de agentes | El agente principal en la auditoría (Fase 0); paró | El humano confirmó el alcance de la tarea |
| La spec Borrador citaba «Error Workflow `005`» en vez de `[ERR] Avisos de error` (constitución VIII) y CA-1 decía «cada abono genera un recibo» aunque el liquidado envía aviso de recogida | Spec redactada antes de fijar convenciones (ADR-0002) | Revisión de la Fase 1 | Corregido en la spec antes de aprobarla |
| Nombre de credencial Gmail inconsistente (`PF · Gmail` en los PRD frente a ADR-0002 sin prefijo `PF ·`) | PRD sin actualizar tras ADR-0002 | Agente principal al preparar el diff de la spec | Elevado al humano, que eligió `Correo tienda` |
| «2 intentos» (spec) frente a «2 reintentos» (encargo a `test-designer`) | Redacción del encargo del agente principal | `test-designer` lo señaló | Se siguió la spec (Max Tries = 2) |
| `pytest` no instalado en local: no se ejecutaron los tests del backend en local | Entorno local incompleto | Al intentar ejecutarlos | La PR no toca `backend/`; pasaron en CI |
| Docker parado durante la auditoría: no se pudo comprobar si `[000]` existía en n8n | Entorno no levantado en la Fase 0 | Auditoría | Se generó 002 sin depender de `[000]` (ver Decisiones) |

### Decisiones

| Propuesta | Decisión | Por qué |
|---|---|---|
| Mostrar `forma_pago` en el recibo (requiere llamada a la API) | Rechazada: no se muestra | La HU no lo pide; evita tratar 401/404 y otra credencial (`API tienda`) |
| Credencial Gmail | Modificada: `Correo tienda`, remitente «Zapatería Paso Firme» | Sin prefijo `PF ·` (ADR-0002) y la misma que propone el plan de 001 |
| Configuración en `$vars` | Modificada: nodo Set `Configuración` | Por si la instancia no tiene Variables |
| `tienda_email` | Aceptada: `tienda@pasofirme.example` | Dirección ficticia, sin datos reales |
| Textos de recibo, recogida y aviso a la tienda propuestos por el agente | Aceptados | Cubren los CA de la spec |
| Retry On Fail 2 intentos + `[ERR] Avisos de error` | Aceptada | Lo pide la spec y la constitución VIII |
| Aplicar el diff de la spec también al plan | Aceptada | Mantener plan y spec alineados |
| Generar 002 sin `[000]` | Aceptada: T-002-03 queda «integración con 000 pendiente» | `[000]` aún no existe ni está decidido cómo pasa `datos` |
| PR con «Closes #11» | Modificada: «Relacionado con #11» | La HU no se cierra hasta la integración y la prueba E2E |
| Bitácora tras aprobar la PR (lo que decía el prompt) | Modificada: ahora, en la misma PR #68 | Decisión de levifvy: quien revisa ve la bitácora junto al flujo |

### Trabajo descartado

- Nodo HTTP `GET /api/apartados/{id}` para obtener la forma de pago.
- `$vars.TIENDA_EMAIL`.
- Formato con `Intl.NumberFormat` / separador de miles: mejora no bloqueante aplazada (`toFixed(2)` da `1234,50 €`).

### Mi prompt o la spec

- La spec Borrador no tenía textos, ni bordes (email vacío o con espacios, talla nula, decimales, zona horaria), ni el nombre de la credencial.
- El prompt asumía que el validador podía fallar por JSON ajenos (no ocurrió: solo existe el 002).
- La cabecera `# SCOPE` contradecía la tarea.

### Lección

Proponer el diff de la spec (textos, bordes, credenciales) antes de aprobarla evitó rehacer el flujo, y evaluar las expresiones del JSON contra las fixtures detecta errores de escapado que el validador estructural no ve.

### Siguientes pasos

- `[000] Enrutador de eventos`: resolver la pregunta abierta en `specs/features/000-*/spec.md:72` (cómo pasa `datos`) e integrar 002 (T-002-03).
- `[ERR] Avisos de error` (spec 005).
- Prueba de extremo a extremo con la app.
- F-002-12: n8n no lanza el Error Workflow en ejecuciones manuales; probarlo en ejecución real.
- Al importar: asignar la credencial `Correo tienda` y el errorWorkflow.
- Revisión humana y aprobación de la PR #68 (T-002-06).

## 2026-10-29 · HU-03 · #12 · Abonos a distancia: puesta en marcha en n8n y revisión de anomalías

- **Persona responsable:** levifvy
- **Herramienta y modelo:** Claude Code (app de escritorio) · Claude Opus 5.5 (`claude-opus-5-5`) como agente principal, conectado a la instancia local de n8n con el MCP de instancia (*Instance-level MCP*, HTTP en `localhost:5678`)
- **Subagente / comando:** agente principal, sin subagentes. No se ha lanzado todavía `/revisar-flujo` (T-003-08)
- **Rama / Spec / PR:** `feature/HU-03-abonos-a-distancia` · `specs/features/003-abonos-a-distancia/` · issue #12 · [PR #70](https://github.com/IA-P1-BCN/zapateria-paso-firme-g2/pull/70) (Draft, con cambios pedidos por BrianStiv) · commits previos `d9a2e80` y `f5d60aa` (2026-10-27) · merge de `develop` `6518b9b` · los cambios de esta sesión en el JSON, `plan.md` y esta bitácora están sin commitear

### Prompt clave

> «Analiza el flujo [003] Abonos a distancia y comprueba las anomalías», repetido después de cada cambio de configuración, y luego peticiones cortas para cada paso: conectar Claude Code con mi n8n, crear las credenciales, montar la Data Table, añadir el aviso de errores, traer `develop` y pasar al repo lo que había cambiado en n8n. Todo en sesiones de pregunta y respuesta, sin un prompt de orquestación largo como en la HU-02.

### Resultado

Empecé el 28 por la tarde con el flujo importado pero sin probar, y lo he dejado funcionando de punta a punta en mi n8n local:

- **Limpieza:** en la instancia había dos `[003]`. Uno juntaba en la misma vista el enrutador, el recibo y el flujo de abonos (41 nodos); lo **archivé**, no lo borré, porque tenía el webhook `/webhook/tienda` que usa la app.
- **Credenciales (T-003-06):**
  - Gmail OAuth2 con la cuenta común de la tienda. Hubo que añadir la URI de redirección de n8n en Google Cloud, meter la cuenta común como usuario de prueba y habilitar la Gmail API.
  - Gemini con una API key de AI Studio creada desde la cuenta común.
  - `API tienda` como Header Auth `X-API-Key`. El agente encontró la cabecera leyendo `backend/middleware/seguridad.py`.
- **Data Table `Emails`** creada con `message_id`, `fecha`, `estado` y `apartado_id`, y asignada en los tres nodos.
- **Primeras ejecuciones manuales:**
  - La ejecución 12 extrajo bien una transferencia de prueba, pero la lancé paso a paso y se quedó en `Pedir apartados activos`, dejando el correo en `en_proceso`. Borré la fila a mano.
  - En la ejecución 13, la IA marcó como `no_pago` un correo mío sin importe y con «abono: efectivo». Acertó: el que estaba mal era mi correo de prueba.
- **Cambios en el flujo:**
  - Quité `Detener por error de la API` y llevé las dos salidas de `¿Error de negocio de la API?` al aviso a Marisa, para que un fallo de la API no corte el bucle.
  - Asigné como Error Workflow el `[ERR] Avisos de error` oficial de develop (005), importado y con la credencial de Gmail puesta.
- **Repo:** fusioné `origin/develop` (sin conflictos, 5/5 flujos válidos). Pasé al JSON y a `plan.md` los cambios de n8n: sin el nodo Detener, `errorWorkflow` = `<<ASIGNAR_EN_N8N>>` como en 001 y 002, modelo `models/gemini-3.5-flash-lite`, desviación explicada en §4 y aviso sobre `down -v` en §5. `validate_workflows.py --estricto`: 5/5 OK.
- **Sin terminar:** las pruebas con los 9 correos. Los envié por Gmail, pero todavía no los he procesado (ver Siguientes pasos).

### Errores o alucinaciones

| Qué hizo mal | Causa raíz | Cómo se detectó | Cómo se corrigió |
|---|---|---|---|
| El agente pidió los detalles de dos workflows con IDs que **se inventó** (`4h5Da…`, `aJh4…`) en vez de los reales | Lanzó en paralelo la búsqueda y la consulta de detalles, y rellenó los IDs antes de tener el resultado | n8n respondió «Workflow not found» | Repitió la consulta con los IDs de la búsqueda (`lNUN…` y `zY37…`) |
| Al principio propuso el conector de n8n del catálogo de Claude, que se conecta desde la nube y no puede llegar a `localhost` | No sabía que mi n8n es local en Docker | Al ver mi captura con `localhost:5678` | Cambió a añadir el MCP de instancia con `claude mcp add --transport http` |
| Al comprobar la conexión imprimió en la conversación el token del MCP completo | Usó `claude mcp get n8n`, que muestra las cabeceras | Lo vio el propio agente en la salida | Me avisó de que quedaba en la sesión y de que lo regenerase si exporto la conversación. Después leyó el token del config sin imprimirlo |
| Dio como ejemplo `avisos@tubanco.es` / `bizum@tubanco.es` para `BANCO_REMITENTES` y yo los copié tal cual en `Configuración` | Ejemplo poco marcado como ficticio | Lo detectó el agente al revisar lo guardado en n8n | Lo dejé solo con el remitente de las pruebas |
| Creó su propio workflow de errores y lo llamó `[000] Avisos de error`, que choca con `[000] Enrutador de eventos` | No había mirado `workflows/README.md`, donde el de errores es `005` → `[ERR]` | Me di cuenta yo al ver el `000-enrutador-eventos.json` en el repo | Lo renombró a `[ERR]`; luego lo sustituimos por el oficial de develop y lo archivó |
| La fixture y la PR dicen que se reinicien los datos con `docker compose down -v`, pero eso también borra el volumen de n8n (flujos, credenciales y la tabla `Emails`) | Instrucción escrita en la sesión del 27 pensando solo en la tienda | El agente revisó el `docker-compose.yml` antes de que lo ejecutara | Reinicio solo de la tienda (`rm -sf tienda` + `volume rm` + `up -d tienda`), ahora documentado en `plan.md` §5 |
| El primer `n8n import:workflow` falló: Git Bash convirtió `/tmp/err.json` en una ruta de Windows | Conversión automática de rutas de MSYS | Error `ENOENT` en la salida | Repetido con `MSYS_NO_PATHCONV=1` |
| Al importar el `[ERR]`, el agente no podía modificarlo | Los workflows importados no tienen el acceso MCP activado | Error «Workflow is not available in MCP» | Lo reimportó sobre el mismo ID desde una copia temporal con `availableInMCP: true`, sin tocar el archivo del repo |
| Envié los 9 correos de prueba de golpe y Gmail parecía haber recibido «solo algunos» | Gmail agrupa los correos con el mismo asunto (01+05, 02+06, 03+07) y reparte el resto en pestañas; además, la ejecución manual del Gmail Trigger solo coge el último correo con la etiqueta | Revisando las ejecuciones (ninguna ese día) y la vista de la etiqueta `Banco` | Procesarlos de uno en uno moviendo la etiqueta `Banco`; para la próxima, añadir «(caso NN)» al asunto |
| El visor de `.eml` de PyCharm mostraba `â□¬` en vez de `€` en el asunto | Los `.eml` no llevan cabeceras MIME y el visor lee el asunto como Latin-1 | Lo vi yo antes de enviar | El archivo está bien en UTF-8; el asunto se copia desde la pestaña *Text* |
| `pytest` no instalado en el Python del sistema | Entorno local incompleto (igual que en la HU-02 y la HU-05) | Al ejecutar los tests | Pendiente de lanzarlos en el entorno `(zapateria)`; la CI ya los pasa |

### Decisiones

| Propuesta | Decisión | Por qué |
|---|---|---|
| Borrar el `[003]` duplicado de 41 nodos | Modificada: archivado | El MCP no permite borrar y, además, ese workflow tenía el webhook de la tienda y el envío de recibos |
| Quitar `Detener por error de la API` | Aceptada (lo hice yo en n8n; el agente lo pasó al JSON y al plan) | Cortaba el bucle y se perdían los demás correos del mismo sondeo. Contrapartida apuntada en `plan.md` §4: un 401 le llega a Marisa como «Pago NO registrado» |
| Mantener el IF `¿Error de negocio de la API?` con las dos salidas al mismo nodo | Aceptada de momento | Así el JSON coincide con mi n8n y se puede tratar el 401 aparte más adelante. Es posible que el revisor diga que sobra |
| Reintentar solos los correos que quedan en `en_proceso` | Rechazada | Se podría registrar el mismo abono dos veces; mejor que avise el Error Workflow y lo revise una persona |
| Usar el `[ERR]` que había creado el agente | Rechazada: se usa el oficial de develop (005) | Lo lleva otro compañero, enmascara datos personales (spec 005) y así no hay dos versiones |
| `errorWorkflow` en el JSON | Modificada: `<<ASIGNAR_EN_N8N>>` en lugar de `<<ID_DE_[ERR]_AVISOS_DE_ERROR>>` | Es lo que usan 001 y 002; el ID cambia en cada instancia |
| Modelo de IA | Aceptada: `models/gemini-3.5-flash-lite` | Suficiente para extraer seis campos y el más barato. Ojo con la capa gratuita y los datos de clientes (ya estaba en los riesgos de la PR) |
| `API_KEY` del `.env` | Modificada: clave aleatoria de 64 caracteres | Tenía puesta por error una API key de mi cuenta de n8n. La tienda solo necesita un secreto compartido con la credencial `API tienda` |
| Probar con Gmail real en vez del flujo `[TEST]` con Form Trigger | Aceptada para esta tanda | Ya tenía Gmail funcionando. Los casos F-003-11a/b siguen necesitando *Pin data* |
| Fusionar `develop` antes de probar | Aceptada | No tocaba nada del 003 ni la tienda y traía el `[ERR]` oficial |

### Trabajo descartado

- El `[ERR] Avisos de error` creado por el agente (Error Trigger + Gmail, sin enmascarado): queda archivado en mi n8n.
- Corregir el horario de revisión duplicado del Gmail Trigger en el JSON: solo existía en mi n8n; el JSON del repo ya estaba bien.

### Mi prompt o la spec

- No conocía bien las convenciones del repo (`workflows/README.md`, la spec 005, los nombres de credenciales). Habría ahorrado vueltas pedirle al agente que las leyera antes de crear nada.
- La spec y la PR daban por hecho el flujo `[TEST]`, y yo acabé probando con Gmail. Hay que dejarlo claro en la PR.
- Otras cosas que salieron al revisar la app (no son de esta HU): `controllers/paginas.py` envía la `API_KEY` al navegador en `window.APP_CONFIG`, y la clave nueva se vio completa en una captura de pantalla.

### Lección

Mirar las ejecuciones y la tabla `Emails` después de cada prueba vale más que fiarse de lo que se ve en Gmail. Y antes de ejecutar cualquier comando que venga de las fixtures o de la PR, conviene comprobar qué hace de verdad. El `down -v` me habría borrado todo n8n.

### Siguientes pasos

- **T-003-07:** procesar los 9 correos de uno en uno (más F-003-10, 11 y 12), rellenar la columna «Obtenido» de las evidencias de la PR y la tabla «Obtenida» de `plan.md` §7.6, y marcar T-003-04…07 en `tasks.md`.
- **T-003-08:** `/revisar-flujo 003` cuando el JSON esté cerrado.
- En n8n: renombrar las credenciales a `Gmail tienda` e `IA extracción` para que coincidan con el repo, y quitar la entrada vacía del horario del Gmail Trigger.
- Cambiar otra vez la `API_KEY` (se vio en una captura) y actualizar la credencial `API tienda`.
- Actualizar la descripción de la PR #70 (sigue hablando de *Stop and Error*), hacer commit y push de los 19 commits pendientes, pasarla a *Ready for review* y volver a pedir revisión a BrianStiv y mmatesanzg23.
- Antes de producción: poner los remitentes reales del banco en `BANCO_REMITENTES` y el correo de Marisa en `MARISA_EMAIL`, y decidir con el equipo cuándo se activa el flujo (es decisión humana).
- Decidir qué hacer con el webhook `/webhook/tienda` (enrutador `[000]`) en mi instancia, para que los recibos de la HU-02 funcionen junto con este flujo.

## 2026-10-29 · HU-05 · Avisos de error (spec 005 → flujo → revisión MCP)

- **Persona responsable:** levifvy
- **Herramienta y modelo:** OpenCode · GLM-5.3-Flash Free (`opencode/glm-5.3-flash-free`) como agente principal orquestador, con MCP `n8n-mcp` contra la instancia local (localhost:5678)
- **Subagente / comando:** `paso-firme-verify` (verificación de la entrega) → `flow-reviewer` (revisión) → `flow-builder` (fix, con confirmación humana) → `ai-scribe` (esta entrada)
- **Rama / Spec / PR:** `feature/HU-05-avisos-errores` · `specs/features/005-error-workflow/` · PR <<PENDIENTE>> · commits `b2ce42d` (feat: `workflows/005-error-workflow.json`) y `fc00bd2` (docs: spec aprobada, plan, tasks, fixtures); el fix del reviewer queda pendiente de commitear

### Prompt clave

> Encargo de verificación de la entrega de la feature 005 / HU-05 (`/paso-firme-verify`) antes de preparar la PR: comprobar el JSON contra el validador del repo, los tests del backend y los esquemas reales de la instancia de n8n (solo lectura); apuntar el veredicto del `flow-reviewer`, aplicar el fix con `flow-builder` y confirmación humana, sincronizar el borrador de la instancia y cerrar con la bitácora.

### Resultado

- Verificación de la entrega con `paso-firme-verify`: `scripts/validate_workflows.py` 3/3 OK, pytest del backend vía uv (13 passed, 0 failed; en el Python del sistema no había pytest), `git diff --check` limpio. Los 4 nodos del flujo validados contra los esquemas de la instancia con `validate_node_config` (4/4 OK, solo lectura). Nota de método: `validate_workflow` del MCP solo acepta código SDK (no JSON exportado), así que el grafo/estructura se valida con el validador del repo y los nodos con `validate_node_config`.
- `flow-reviewer`: **CAMBIOS NECESARIOS**. 1 bloqueante: la regex de secretos `\b[A-Za-z0-9_-]{32,}\b` dejaba pasar segmentos centrales de JWT con puntos decodificables, y el mensaje se recortaba a 600 caracteres ANTES de enmascarar (un token cortado por la mitad quedaba en trozos <32 y escapaba). Mejoras: teléfonos con prefijo 34 pegado, fallback de mensaje sin `errorEjec` y `webhookId` cruft en el nodo Gmail, checkbox T-005-02.
- Fix aplicado por `flow-builder` con confirmación de la usuaria: regex de JWT añadida antes de la de 32+, enmascarar antes de recortar, `(?:34)?` en teléfonos, `errorEjec` añadido al fallback de mensaje, `webhookId` eliminado del JSON, T-005-02 marcada y caso JWT añadido a la fixture F-005-2. Re-ejecutado `validate_workflows.py` (3/3 OK) y prueba del enmascaramiento fuera de n8n (node) correcta.
- El borrador `[ERR]` ya importado en la instancia (id `9JXk22pXHSDwT19U`, `active: false`) se sincronizó vía `update_workflow` (operación `updateNodeParameters` del `jsCode` del Code, `versionName` «Fix masking JWT»). NO se activó ni se publicó (regla 3).

### Errores o alucinaciones

No se registraron alucinaciones relevantes del modelo en esta sesión. Problemas detectados y su tratamiento:

| Qué hizo mal | Causa raíz | Cómo se detectó | Cómo se corrigió |
|---|---|---|---|
| `ai-scribe` (1.er intento): la respuesta se cortó y la entrada no llegó a escribirse | Respuesta incompleta del modelo | Falta de la entrada al cerrar la tarea | Se reanudó la sesión y se reescribió esta entrada |
| `flow-reviewer` validó el enmascaramiento sobre la copia importada en la instancia y no sobre el JSON del repo | El `jsCode` se trunca al leerlo del JSON del repo (limitación de lectura, no del código) | Al leer `workflows/005-error-workflow.json` | Se validó contra el borrador `9JXk22pXHSDwT19U` de la instancia (y el fix sincronizó repo e instancia) |
| `pytest` ausente en el Python del sistema | Entorno local incompleto | Al ejecutar los tests del backend | Se ejecutaron con `uv run --with-requirements`; sin modificar tests ni probar el flujo para que pase |
| `validate_workflow` del MCP rechaza JSON exportado (solo acepta código SDK) | Diseño del MCP n8n-mcp | Al intentar validar el grafo completo con el MCP | Se validaron los 4 nodos con `validate_node_config` y la estructura/grafo con `scripts/validate_workflows.py` del repo |

### Decisiones

| Propuesta | Decisión | Por qué |
|---|---|---|
| Mantener `.opencode/opencode.jsonc` (modificado) fuera de esta PR | Aceptada | Cambio de infraestructura no relacionado con la HU; el humano decide más adelante si se commitea aparte |
| `flow-builder` aplicó el fix del reviewer | Aceptada | Spec 005 Aprobada + confirmación humana de levifvy (ADR-0002, D10) |
| Sincronizar el borrador de la instancia vía `update_workflow` | Aceptada | Mantener n8n y repo alineados; sin activar ni publicar (regla 3) |
| Credencial «Gmail account» (id `JRceb88QuejfOdfA`, la misma que usa el flujo 001) | Modificada: renombrar a «Gmail tienda» en la UI de n8n | Es una acción de credenciales de la instancia, no del JSON; no se toca n8n más allá del borrador del flujo |
| Push / PR / activación final | Aceptada: quedan en manos del humano (regla 4) | El agente no hace push ni activa flujos |

### Siguientes pasos

- Commitear el fix (`workflows/005-error-workflow.json`, fixtures, `tasks.md`), push de la rama y abrir la PR (humano).
- En la UI de n8n: renombrar la credencial a «Gmail tienda» (unificar el nombre con el resto), cambiar el destinatario por el correo real (el fijo de Levi y el del sticky), asignar `[ERR]` como Error Workflow en los Settings del resto de flujos (CA-3) y activarlo al final (última decisión del humano).
- Probar el aviso en condiciones reales: el Error Trigger no se dispara en ejecuciones manuales; forzar un fallo en producción de un flujo de prueba.
- Eliminar el flujo duplicado de `[000]` + `[001]` (id `KfQpai0qg9BtrmVr`) de la instancia.

## 2026-10-29 · HU-03 · T-003-07 · Abonos a distancia: prueba con los 9 correos del banco

- **Persona responsable:** levifvy
- **Herramienta y modelo:** Claude Code (app de escritorio) · Claude Opus 5.5 (`claude-opus-5-5`), con el MCP de instancia de n8n para leer las ejecuciones y la Data Table. En el flujo, Gemini `models/gemini-3.5-flash-lite`
- **Subagente / comando:** agente principal, sin subagentes. `/revisar-flujo` (T-003-08) todavía pendiente
- **Rama / Spec / PR:** `feature/HU-03-abonos-a-distancia` · `specs/features/003-abonos-a-distancia/` · issue #12 · [PR #70](https://github.com/IA-P1-BCN/zapateria-paso-firme-g2/pull/70)

### Prompt clave

> «Ya hice la ejecución de todos los correos, ¿qué sigue para que la PR pueda ser aprobada?». Antes de eso, una ronda de preguntas cortas mientras probaba: por qué no llegaban los correos, cómo identificar cada uno en Gmail y cómo dejar solo uno con la etiqueta `Banco`.

### Resultado

Reinicié solo la tienda, vacié la Data Table `Emails` y probé los 9 `.eml` reenviándolos desde mi cuenta al buzón de la tienda. Los procesé de uno en uno: ponía la etiqueta `Banco` a un correo y lanzaba *Execute workflow*. El agente revisó cada ejecución por MCP y comparó con la API de la tienda.

| Caso | Ejec. | Resultado | ¿Esperado? |
|---|---|---|---|
| F-003-1 Carmen | 14 | Registra 10 € (apartado 1: 19,50 → 9,50) | ✅ |
| F-003-2 Jorge | 15 | Registra 20 € por la referencia «apartado 2» (79 → 59) | ✅ |
| F-003-3 Lucía | 16 | Registra 12 € como `bizum`, queda **liquidado**; aviso de transferencia a Marisa | ✅ |
| F-003-4 Laura | 17 | No registra (15 € > 10 € pendientes); aviso a Marisa; `rechazado` · 12 | ✅ |
| F-003-5 Romero | 18 | No registra; pregunta a Marisa; `dudoso` | ✅ (motivo distinto, ver abajo) |
| F-003-6 Paula | 19 | No registra (plazo vencido); aviso a Marisa; `rechazado` · 16 | ✅ |
| F-003-7 Antonio | 20 | No registra (cliente desconocido); pregunta a Marisa; `dudoso` | ✅ |
| F-003-8 Publicidad | 21 | `no_pago` → `ignorado`, sin aviso | ✅ |
| F-003-9 Silvia | 22 | Registra 5 € aunque en la app lleva tilde (35 → 30) | ✅ |
| F-003-10 Duplicado | 23 | `¿Ya procesado?` → sí; no llama a la IA ni a la API | ✅ |

En la tienda solo aparecen abonos nuevos en los apartados 1, 2, 3 y 24. Se mandaron los 5 avisos a Marisa que tocaban. F-003-11a/b y F-003-12 no los hice porque el briefing solo pide que el flujo resuelva bien los correos de `data/correos/`; quedan pendientes en la PR.

### Errores o alucinaciones

La IA de extracción no inventó ningún dato. Los problemas vinieron de cómo preparé las pruebas:

| Qué hizo mal | Causa raíz | Cómo se detectó | Cómo se corrigió |
|---|---|---|---|
| Parecía que «solo llegaban algunos correos» | Gmail mandó a **Spam** 12 de los 18 correos (los que imitan un aviso de banco desde una cuenta personal), y `from:` no busca en Spam | El agente lo sospechó por el patrón de los que faltaban; lo confirmé en la carpeta Spam | «No es spam» y filtro «No marcar nunca como spam» para mi remitente |
| Mi filtro de Gmail ponía la etiqueta `Banco` a todo lo que yo enviaba | Lo había creado así para las pruebas del día anterior | El agente vio la etiqueta en los correos que estaban en Spam | Quité esa acción del filtro; la etiqueta la pongo a mano, correo a correo |
| La segunda tanda de envíos (11:23–11:28) salió mal: en el «Bizum de 20,00 €» pegué el texto de Carmen y en el de Romero se juntaron las líneas | Copiar y pegar a mano nueve correos seguidos | El agente revisó la lista de *Enviados* antes de procesarlos | Esa tanda no se usó; se probó solo con la primera |
| Al principio no había ninguna ejecución, aunque yo creía haber probado | Solo había enviado los correos, sin pulsar *Execute workflow* | El agente no encontró ejecuciones ni filas en `Emails` | Procesar cada correo a mano después de etiquetarlo |
| En F-003-5 la IA devolvió como concepto «El importe ya está disponible en tu cuenta» (la fixture espera `null`) | Al pegar el correo en Gmail se perdieron los saltos de línea y esa frase quedó justo detrás de «Concepto:» | Comparando el cuerpo que recibió n8n con el `.eml` | No se cambió nada: con ese texto la extracción es razonable y el caso sigue saliendo dudoso. El motivo cambia («el concepto no coincide» en vez de «nombre abreviado sin concepto»). Anotado en `plan.md` §7.6 |

### Decisiones

| Propuesta | Decisión | Por qué |
|---|---|---|
| Probar con Gmail real en vez del flujo `[TEST]` con Form Trigger | Aceptada | Ya tenía Gmail funcionando y así se prueba también el disparador de verdad |
| Desactivar la vista de conversación en el Gmail de la tienda | Aceptada | Con conversaciones, la etiqueta se pone a todos los correos con el mismo asunto (01+05, 02+06, 03+07) y n8n cogería el que no toca |
| F-003-11a/b y F-003-12 | Pendientes | No los exige el briefing; los pide `fixtures.md` como casos extra |
| Repetir F-003-5 con el formato exacto del `.eml` | Rechazada por ahora | El resultado final es el mismo (pregunta a Marisa, no registra) |
| Cambiar en `fixtures.md` el reinicio con `docker compose down -v` | Aceptada | Borraba también n8n; ahora se reinicia solo la tienda |

### Lección

En producción, que Gmail mande a Spam un aviso del banco es un riesgo real: n8n no lee el Spam, y ese pago no se procesaría sin que nadie se enterara. Hay que crear en la cuenta de la tienda un filtro «No marcar nunca como spam» para los remitentes reales del banco antes de activar el flujo.

### Siguientes pasos

- `/revisar-flujo 003` (T-003-08) y, si sale APROBADO, pasar la PR #70 a *Ready for review* y volver a pedir revisión a BrianStiv.
- Antes de activar: remitentes reales del banco en `BANCO_REMITENTES` y en el filtro anti-spam, y el correo de Marisa en `MARISA_EMAIL`.
- Opcional: F-003-11a/b (con *pinned data*) y F-003-12.

## 2026-10-27 · 000 · T-000-07 · Enrutador de eventos (spec 000 → flujo)

- **Persona responsable:** Miguel Matesanz (`mmatesanzg23`)
- **Herramienta y modelo:** OpenCode · big-pickle
- **Subagente / comando:** agente principal; según `tasks.md`: `test-designer` (fixtures) → `flow-builder` (JSON) → `flow-reviewer` (revisión). Sin n8n-mcp.
- **Rama / Spec / PR:** `feature/HU-00-enrutador-eventos` · `specs/features/000-enrutador-eventos/` · PR <<PENDIENTE>> (T-000-06) · commit `7a037d4`

### Prompt clave

> <<PENDIENTE: prompts exactos de la sesión no disponibles; resumidos, sin datos personales ni claves>>

### Resultado

- Spec 000 de Borrador a Aprobada (aprueba Levi Flores, 2026-10-27); plan, tareas y fixtures (4 eventos + 3 fallback) completos.
- Flujo `[000] Enrutador de eventos`: Webhook `POST /webhook/tienda` (Respond Immediately) → Switch por `{{ $json.body.evento }}` con fallback → 5 ramas No Op (`apartado.creado`, `abono.registrado`, `venta.registrada`, `apartado.vencido`, evento desconocido). `active: false`, sin credenciales.
- `flow-reviewer`: APROBADO CON OBSERVACIONES (sin bloqueantes); única observación: `settings.errorWorkflow` aplazado a T-000-08.
- `validate_workflows.py`: OK. CA-1…CA-4 verificados con fixtures.

### Errores o alucinaciones

No se registraron alucinaciones. Observación del reviewer: `settings.errorWorkflow` no asignado hasta que exista `005`.

### Decisiones

| Propuesta | Decisión | Por qué |
|---|---|---|
| Sub-flujos por evento (Execute Workflow) | Aceptada | Permite a 3 personas trabajar en paralelo sin pisar el mismo JSON |
| Responder de inmediato en el Webhook | Aceptada | La app corta a los 5 s |
| No Ops provisionales para 001/002 | Aceptada | Cableado en T-000-08 |
| Asignar Error Workflow ahora | Rechazada (aplazada) | `005` aún no existía |

### Siguientes pasos

- T-000-06: PR y revisión humana (Levi).
- T-000-08: cablear Execute Workflow a 001/002 y asignar Error Workflow 005.

## 2026-10-29 · 004 · T-004-08 · Cierre diario (spec 004 → flujo)

- **Persona responsable:** Miguel Matesanz (`mmatesanzg23`)
- **Herramienta y modelo:** OpenCode · big-pickle
- **Subagente / comando:** agente principal; según `tasks.md`: `test-designer` (fixtures) → `flow-builder` (JSON) → `flow-reviewer` + `api-contract-checker` (revisión). Sin n8n-mcp.
- **Rama / Spec / PR:** `feature/HU-04-cierre-diario` · `specs/features/004-cierre-diario/` · PR <<PENDIENTE>> (T-004-07) · commit `9938956`

### Prompt clave

> <<PENDIENTE: prompts exactos de la sesión no disponibles; resumidos, sin datos personales ni claves>>

### Resultado

- Spec 004 de Borrador a Aprobada (aprueba Levi Flores, 2026-10-28); plan, tareas y fixtures (F-004-1…F-004-3) completos.
- Flujo `[004] Cierre diario`: Schedule Trigger 21:30 Europe/Madrid → `Fecha de hoy` → `Pedir ventas del día` (GET /api/ventas) → `Pedir abonos del día` (GET /api/abonos) → `Sumar por forma de pago` (Code) → `Guardar cierre en Google Sheets` (upsert por `fecha`) → `Enviar resumen a Marisa` (Gmail). `active: false`.
- `alwaysOutputData: true` en ambos HTTP; retryOnFail (2 intentos, 3 s) en HTTP, Sheets y Gmail; errorWorkflow `[ERR] Avisos de error`.
- T-004-01, T-004-02, T-004-03 y T-004-06 marcadas como hechas; T-004-04 (credenciales/hoja), T-004-05 (prueba) y T-004-07 (PR) pendientes.

### Errores o alucinaciones

No se registraron alucinaciones relevantes. <<PENDIENTE: pegar veredicto de `flow-reviewer`/`api-contract-checker` si se registró>>

### Decisiones

| Propuesta | Decisión | Por qué |
|---|---|---|
| Consultar la API (GET ventas/abonos) | Aceptada | Los avisos del webhook no tienen reintentos y pueden perderse |
| Redondear solo cada total resultante (`Math.round(total * 100) / 100`) | Aceptada | Constitución I y ADR-0002 D6 (evita `0.30000000000000004`) |
| Upsert por `fecha` en Google Sheets | Aceptada | Si se ejecuta dos veces el mismo día, actualiza la fila sin duplicar |

### Siguientes pasos

- T-004-04: crear credenciales (`API tienda`, Google Sheets, Gmail) y hoja `Cierres`.
- T-004-05: probar con datos de ejemplo y comparar con la app.
- T-004-07: PR y revisión humana (Brian).
