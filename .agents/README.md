# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# .agents/ · Capa de trabajo con agentes

Fuente única de lo que es **común a todas las herramientas** de IA. Las herramientas leen copias generadas o carpetas compatibles.

## Qué hay y quién lo lee

| Pieza | Fuente (editar aquí) | Claude Code lee | OpenCode lee |
|---|---|---|---|
| Reglas del proyecto | `AGENTS.md` | `CLAUDE.md` → `@AGENTS.md` | `AGENTS.md` |
| Skills | `.claude/skills/<nombre>/SKILL.md` | `.claude/skills/` (solo esta carpeta) | `.opencode/skills/` (generado) y, por compatibilidad, `.claude/skills/` |
| Subagentes | `.agents/agents/<nombre>.md` + metadatos en `scripts/sync_agents.py` | `.claude/agents/` (generado) | `.opencode/agents/` (generado) |
| Comandos | `.agents/commands/<nombre>.md` + metadatos en `scripts/sync_agents.py` | `.claude/commands/` (generado) | `.opencode/commands/` (generado) |
| Permisos | — | `.claude/settings.json` | `.opencode/opencode.jsonc` |
| Equipo y reparto | `.agents/team.md` | bajo demanda | bajo demanda |
| Decisiones de arquitectura | `.agents/decisions/` | bajo demanda | bajo demanda |
| Plantilla de la bitácora | `.agents/templates/ai-log-entry.md` | bajo demanda | bajo demanda |
| Plantilla de PR | `.github/PULL_REQUEST_TEMPLATE.md` (única) | GitHub | GitHub |

Las skills se editan **solo** en `.claude/skills/`. `scripts/sync_agents.py` las copia a `.opencode/skills/` (carpeta propia de OpenCode; no se edita a mano) y `sync_agents.py --check` / el validador avisan si una copia queda desactualizada. Se copian en lugar de usar enlaces simbólicos porque en Windows los enlaces exigen modo desarrollador. `.agents/skills/` ya no existe. Ver `decisions/ADR-0002-convenciones-flujos.md` (D7–D9).

| Tipo | Skills |
|---|---|
| Del proyecto | `sdd-workflow`, `dominio-apartados`, `tienda-api`, `n8n-convenciones`, `n8n-import-export`, `revision-seguridad-flujos`, `datos-de-prueba`, `trazabilidad-ia` |
| Del equipo (antes solo en OpenCode) | `paso-firme-review`, `paso-firme-verify` (en OpenCode también como comandos `/paso-firme-*`) |
| Externas adaptadas (*fork*, no se actualizan con `npx skills update`) | `n8n-expression-syntax`, `n8n-code-javascript`, `n8n-workflow-patterns` — llevan una nota: prevalecen `AGENTS.md` y las skills del proyecto |

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

## Subagentes

| Nombre | Permisos | Precarga skills |
|---|---|---|
| `spec-writer` | Lee todo; escribe en `specs/` | `sdd-workflow`, `dominio-apartados`, `n8n-convenciones`, `tienda-api` |
| `flow-builder` | Lee todo; escribe en `workflows/` y `tasks.md` (con confirmación) | `n8n-convenciones`, `tienda-api`, `dominio-apartados`, `n8n-import-export` |
| `flow-reviewer` | Solo lectura | `revision-seguridad-flujos`, `n8n-convenciones`, `tienda-api`, `dominio-apartados` |
| `api-contract-checker` | Solo lectura | `tienda-api` |
| `test-designer` | Escribe `fixtures.md` | `datos-de-prueba`, `tienda-api` |
| `ai-scribe` | Escribe `docs/ai-log.md` | `trazabilidad-ia` |

## Orquestación

Los subagentes **no se llaman entre sí**: cada uno trabaja en su contexto aislado y devuelve un resumen. Orquesta el agente principal (o el comando `/…` que lo invoca), con una persona revisando entre pasos:

```
spec-writer (/sdd-spec) ─▶ aprobación humana ─▶ /sdd-plan + api-contract-checker ─▶ /sdd-tasks
   ─▶ test-designer (fixtures) ─▶ flow-builder (/construir-flujo) ─▶ flow-reviewer + api-contract-checker (/revisar-flujo)
   ─▶ PR con revisión humana ─▶ ai-scribe (/bitacora)
```
