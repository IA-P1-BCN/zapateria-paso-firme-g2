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
