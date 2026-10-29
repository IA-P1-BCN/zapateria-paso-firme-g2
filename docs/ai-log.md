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
