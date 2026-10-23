# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# ADR-0001 · Estructura de la capa de agentes

- **Estado:** Propuesta (pendiente de aprobación del equipo)
- **Fecha:** 2026-10-23
- **Rama:** `feature/HU-agentic-work`

## Contexto

El equipo (3 personas) usará OpenCode y posiblemente Claude Code para construir flujos n8n alrededor de una app existente que no se debe modificar. Hace falta una capa común de reglas, skills, subagentes y SDD que funcione en ambas herramientas sin duplicar contenido.

## Decisiones

| # | Decisión | Alternativas | Motivo |
|---|---|---|---|
| D1 | `AGENTS.md` es la fuente de reglas; `CLAUDE.md` solo lo importa (`@AGENTS.md`) y añade lo específico de Claude | Dos archivos completos | Un único sitio que mantener |
| D2 | Skills: fuente en `.claude/skills/`, copia generada en `.opencode/skills/` por `scripts/sync_agents.py` | `.agents/skills/`; una sola carpeta compartida | Claude Code no lee `.agents/skills/`. OpenCode también lee `.claude/skills/`, pero el equipo trabaja con OpenCode y pidió tenerlas en su carpeta (2026-10-23); al ser generadas no se editan dos veces |
| D3 | Subagentes y comandos: cuerpo en `.agents/`, metadatos en `scripts/sync_agents.py`, copias generadas por herramienta | Escribirlos a mano dos veces | El frontmatter de Claude Code y de OpenCode es distinto (tools/skills frente a mode/permission) |
| D4 | La línea `# SCOPE` va **dentro** del frontmatter YAML en archivos que lo requieren (SKILL.md, subagentes, comandos) | Antes del `---` | El frontmatter tiene que empezar en la línea 1 para que las herramientas lo lean |
| D5 | `.claude/settings.json` no lleva la línea `# SCOPE` | Añadir una clave extra | JSON no admite comentarios y una clave desconocida podría invalidar los ajustes. `opencode.jsonc` sí la lleva como comentario |
| D6 | Scripts en Python (sin dependencias) | Bash | El equipo trabaja en Windows y el proyecto ya usa Python |
| D7 | No se crea `.mcp.json` en la raíz; n8n-mcp se documenta para añadirlo en ámbito local (Claude) y desactivado en `opencode.jsonc` | `.mcp.json` compartido | La regla de alcance solo permite 3 archivos en la raíz y así ninguna clave llega al repo |
| D8 | Nombre de flujo con el número de su spec (`[004] Cierre diario`) | Número de flujo del enunciado | Un solo número para spec, archivo y flujo |

## Ambigüedades resueltas de forma conservadora

| Ambigüedad | Decisión |
|---|---|
| El prompt dice que el frontend es React; en el repo es HTML/CSS/JS plano | Se documenta como HTML/JS plano. No se ha tocado |
| El prompt dice que los flujos van en `automation/`; el enunciado pide `workflows/` y ninguna existe | Se usa `automation/` como nombre provisional con `<<PENDIENTE>>` en todas partes. No se crea ninguna de las dos |
| La bitácora de IA es `docs/ai-log.md` (entregable) pero `docs/` no está en las rutas permitidas | No se crea; lo creará `ai-scribe` en su primer uso. La plantilla está en `.agents/templates/` |
| Proteger el webhook (HU-14) exigiría que la app enviara una cabecera | No se toca el backend; queda como bloqueo en `specs/backlog.md` |
| `transferencia` no es forma de pago válida en la app | Queda como `<<PENDIENTE>>` en la spec 003 y en la ontología |
| No está claro si OpenCode carga `.opencode/opencode.jsonc` en todas las versiones | Se usa esa ruta (las reglas no permiten `opencode.json` en la raíz). Si no se carga: `OPENCODE_CONFIG=.opencode/opencode.jsonc opencode` |
| Las specs 000–005 se escriben en `Borrador` | Ningún agente puede aprobarlas; lo hace el equipo |

## Consecuencias

- Al editar un subagente o comando hay que ejecutar `python scripts/sync_agents.py` (`validate_agent_infra.py` lo detecta si se olvida).
- Los permisos de Claude Code bloquean `backend/` y `frontend/`; OpenCode pide confirmación en cada edición (`"edit": "ask"`) porque su configuración es más simple.
