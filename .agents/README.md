# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# .agents/ · Capa de trabajo con agentes

Fuente única de lo que es **común a todas las herramientas** de IA. Las herramientas leen copias generadas o carpetas compatibles.

## Qué hay y quién lo lee

| Pieza | Fuente (editar aquí) | Claude Code lee | OpenCode lee |
|---|---|---|---|
| Reglas del proyecto | `AGENTS.md` | `CLAUDE.md` → `@AGENTS.md` | `AGENTS.md` |
| Skills | `.claude/skills/<nombre>/SKILL.md` | igual | `.opencode/skills/` (generado) |
| Subagentes | `.agents/agents/<nombre>.md` + metadatos en `scripts/sync_agents.py` | `.claude/agents/` (generado) | `.opencode/agents/` (generado) |
| Comandos | `.agents/commands/<nombre>.md` + metadatos en `scripts/sync_agents.py` | `.claude/commands/` (generado) | `.opencode/commands/` (generado) |
| Permisos | — | `.claude/settings.json` | `.opencode/opencode.jsonc` |
| Equipo y reparto | `.agents/team.md` | bajo demanda | bajo demanda |
| Decisiones de arquitectura | `.agents/decisions/` | bajo demanda | bajo demanda |
| Plantillas (bitácora, PR) | `.agents/templates/` | bajo demanda | bajo demanda |

Las skills se editan en `.claude/skills/` (Claude Code no lee `.agents/skills/`). `scripts/sync_agents.py` las copia a `.opencode/skills/`, la carpeta propia de OpenCode, para que el equipo las encuentre ahí; el validador avisa si una copia queda desactualizada. Ver `decisions/ADR-0001-infraestructura-agentes.md` (D2).

## Flujo de edición

```bash
# 1. Editar el cuerpo de un subagente o comando
#    .agents/agents/flow-builder.md   o   .agents/commands/revisar-flujo.md
# 2. (Si cambian herramientas/permisos/descripción) editar AGENTS / COMMANDS en scripts/sync_agents.py
# 3. Regenerar
python scripts/sync_agents.py
# 4. Validar antes de la PR
python scripts/validate_agent_infra.py
```

Nunca edites a mano `.claude/agents/`, `.claude/commands/`, `.opencode/agents/` ni `.opencode/commands/`: se sobrescriben.

## Miniagentes

| Nombre | Permisos | Precarga skills |
|---|---|---|
| `spec-writer` | Lee todo; escribe en `specs/` | `sdd-workflow`, `dominio-apartados`, `tienda-api` |
| `flow-builder` | Lee todo; escribe en `automation/` y `tasks.md` (con confirmación) | `n8n-convenciones`, `tienda-api`, `dominio-apartados`, `n8n-import-export` |
| `flow-reviewer` | Solo lectura | `revision-seguridad-flujos`, `n8n-convenciones`, `dominio-apartados` |
| `api-contract-checker` | Solo lectura | `tienda-api` |
| `test-designer` | Escribe `fixtures.md` | `datos-de-prueba`, `tienda-api` |
| `ai-scribe` | Escribe `docs/ai-log.md` | `trazabilidad-ia` |
