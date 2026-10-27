# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# ADR-0002 · Convenciones de flujos y orden de la capa de agentes

- **Estado:** Aprobada (2026-10-27)
- **Fecha:** 2026-10-25
- **Rama:** `feature/HU-agentic-work2-v2`
- **Sustituye en parte a:** ADR-0001 (ambigüedad «carpeta de flujos» y D2 sobre dónde viven las skills)
- **Origen:** informe de incompatibilidades entre la capa de agentes y los archivos añadidos por el equipo (2026-10-23)

## Contexto

Las piezas añadidas por el equipo (`CONTRIBUTING.md`, `flujos/`, la CI, las skills externas de `.agents/skills/`, las skills `paso-firme-*` y los PRD) seguían convenciones distintas de la capa de agentes: tres carpetas para los flujos, tres esquemas de nombres, tres nombres para la credencial de la API y skills que ordenaban activar o publicar flujos (regla dura 3). Un agente que leía ambas fuentes recibía órdenes contradictorias.

## Decisiones

| # | Decisión | Alternativas descartadas | Motivo |
|---|---|---|---|
| D1 | **Carpeta única de flujos: `workflows/`**. `flujos/` se renombra (conserva su README). `automation/` deja de usarse | `automation/`, `flujos/` | La pide el enunciado (entregable 2) y ya la usan los PRD |
| D2 | **Archivo: `workflows/NNN-slug.json`** con el número de 3 dígitos de su spec (`004-cierre-diario.json`) | `NN-…` (nº del enunciado, 2 dígitos); `fl-0x-…` (PRD) | Un solo número encadena spec, plan, tasks, fixtures y JSON |
| D3 | **Nombre en n8n: `[NNN] Nombre`**; sub-flujos `[SUB] …`; Error Workflow `[ERR] Avisos de error`; enrutador `[000] Enrutador de eventos` | `PF · FL-0X · …` (PRD); `Daily: …` (skill externa) | Ya estaba en `AGENTS.md` y `n8n-convenciones`; el prefijo `[NNN]` coincide con el archivo |
| D4 | **Trazabilidad con el enunciado**: cada spec lleva en su cabecera `- **Flujo enunciado:** FL-XX` (o `—` si no corresponde a un flujo del enunciado). La tabla de equivalencias está en `workflows/README.md` y `specs/backlog.md` | Renumerar las specs al nº del enunciado | No se pierde el número FL y no se rompe la numeración existente |
| D5 | **Credencial de la API: `API tienda`** (Header Auth, cabecera `X-API-Key`) | `PF · API tienda` (PRD), `API Paso Firme` (paso-firme-review) | Era el nombre de `n8n-convenciones`, `tienda-api` y los planes. En n8n el nombre tiene que coincidir exactamente |
| D6 | **Redondeo**: nunca se redondea ni se altera un importe que da la app (`importe`, `abonado`, `pendiente`, vale). Al **sumar** movimientos (cierre diario, informe mensual) solo se redondea el **total resultante** a 2 decimales (`Math.round(total * 100) / 100`, o sumando en céntimos), para eliminar el error de coma flotante (`0.1 + 0.2`). No se redondea cada sumando | «Sin redondear» literal (dejaría `0,30000000000000004`); redondear cada importe | Respeta la regla 5 (no recalcular lo que da la app) y el caso `F-004-3` de los fixtures |
| D7 | **Skills: fuente única en `.claude/skills/`**; `scripts/sync_agents.py` las copia a `.opencode/skills/` (generadas, no se editan). `.agents/skills/` deja de existir | Enlaces simbólicos; mantener `.agents/skills/` como carpeta neutral | Claude Code solo lee `.claude/skills/`. Los enlaces simbólicos en Windows exigen modo desarrollador y `core.symlinks`, y el equipo trabaja en Windows. La copia ya la valida `sync_agents.py --check` |
| D8 | **Skills externas** (ver tabla de abajo): se adaptan y se mueven a `.claude/skills/` las que aportan; se eliminan las que contradicen las reglas duras o no aplican | Dejarlas tal cual en `.agents/skills/` | Claude Code no las veía, y varias ordenaban activar o publicar flujos |
| D9 | **Skills `paso-firme-review` y `paso-firme-verify`**: fuente en `.claude/skills/`; sus comandos en `.agents/commands/` (generados para ambas herramientas) | Dejarlas solo en `.opencode/` | `.opencode/` es una carpeta generada y quien usa Claude Code no las tenía |
| D10 | **Cabecera SCOPE**: `# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)`. Solo `flow-builder` usa `# SCOPE: infraestructura-agentes (NO tocar backend/frontend; workflows/ solo flow-builder)` | Mantener `automation` en la cabecera | `automation/` ya no existe y `flow-builder` es justo quien debe escribir en `workflows/` |
| D11 | **`python`, no `python3`**, en skills, permisos de Claude Code/OpenCode y CI (en CI con `actions/setup-python`, que garantiza el comando) | `python3` | En Windows `python3` puede no existir y los permisos solo permitían `python …` |
| D12 | **Canal único Gmail** para clientes y tienda, y **transferencia → `bizum`** (indicando a Marisa que el origen era una transferencia). Se pasan a las specs | Mantener `<<PENDIENTE>>` | Ya lo decidieron los PRD (`docs/prd-nivel-medio.md` §1 y §6.4). El mapeo de transferencias sigue siendo un supuesto a confirmar con Marisa |
| D13 | **Orquestación**: los subagentes no se llaman entre sí. El agente principal (o el comando `/…`) orquesta `spec-writer` → aprobación humana → `/sdd-plan` y `/sdd-tasks` → `flow-builder` → `flow-reviewer` + `api-contract-checker` → `ai-scribe` | Subagentes que delegan en otros | Contexto aislado y trazable; cada paso lo revisa una persona |
| D14 | **Una sola plantilla de PR**: `.github/PULL_REQUEST_TEMPLATE.md`. Se elimina `.agents/templates/pr-checklist.md` | Mantener las dos | Estaban duplicadas y la de GitHub es la que se usa al abrir la PR |

### Skills externas (D8)

| Skill (origen) | Decisión | Motivo |
|---|---|---|
| `n8n-expression-syntax` (czlonkowski/n8n-skills) | **Se queda**, adaptada | Útil para expresiones. Se añade la nota de precedencia y se avisa de que `$env` no se usa en este proyecto (`$vars` o nodo `Configuración`) |
| `n8n-code-javascript` (czlonkowski/n8n-skills) | **Se queda**, adaptada | Útil para nodos Code. Se eliminan las partes que enseñan a hacer HTTP desde un nodo Code (`this.helpers.httpRequest`); en este proyecto eso va en un nodo HTTP Request |
| `n8n-workflow-patterns` (czlonkowski/n8n-skills) | **Se queda**, adaptada | Patrones de webhook, HTTP y programados. Se quitan el paso «activar el flujo», las herramientas de gestión del MCP que crean, despliegan o activan flujos, el patrón de base de datos (no aplica: todo va por la API) y el «el agente decide y actúa» (regla 6) |
| `n8n-workflow-lifecycle-official` (n8n-io/skills) | **Se elimina** | Todo el ciclo gira en torno a `publish_workflow` y al MCP oficial de n8n, que el proyecto no usa. Sus nombres en inglés contradicen D3. Su contenido útil ya está en `n8n-convenciones`, `n8n-import-export` y `revision-seguridad-flujos` |
| `n8n-debugging-official` (n8n-io/skills) | **Se elimina** | Se apoya en herramientas del MCP oficial (`get_workflow_execution`, `get_node_types`…) que no existen en `n8n-mcp`, y cita skills no instaladas. Pendiente: si el equipo la echa de menos, reescribir una `n8n-depuracion` propia |
| `fastapi-patterns` (affaan-m/ecc) | **Se elimina** | Enseña a programar el backend, que no se puede tocar |
| `conventional-git` (samber/cc-skills) | **Se elimina** | Los agentes no hacen commits (regla 4). Contradice las ramas `feature/HU-XX-slug` y la atribución de IA que pide la trazabilidad. La convención de commits vive en `CONTRIBUTING.md` (pendiente de consensuar) |

Las skills adaptadas son un *fork*: **no** se actualizan con `npx skills update` (sobrescribiría las adaptaciones y las reinstalaría en `.agents/skills/`). `skills-lock.json` se conserva solo como registro de procedencia de las tres que se quedan.

## Pendiente de consensuar con el equipo (no se cambia de forma unilateral)

- `docs/prd-*.md` y `docs/diagramas/`: usan `PF · FL-0X · …`, `workflows/fl-0x-….json` y la credencial `PF · API tienda`. Si se aprueba este ADR, hay que actualizarlos (o, si el equipo prefiere el esquema de los PRD, cambiar este ADR).
- `CONTRIBUTING.md`: prefijos de rama (`flujo/`, `feat/` para backend) frente a `feature/HU-XX-slug`, tipos de commit frente a los que acepta la CI, idioma de los commits.
- `.github/workflows/ci.yml`: activar el job `infra-agentes` (preparado y comentado al final del archivo) y cambiar `python3` por `python` con `actions/setup-python` en los jobs actuales (D11).
- `scripts/gemini_review.py` envía el diff de `specs/` y fixtures a un modelo externo (regla 10, RGPD): valorar excluir `specs/**/fixtures.md`.

## Consecuencias

- `scripts/validate_agent_infra.py` comprueba esta estructura: cabecera SCOPE, skills solo en `.claude/skills/`, copias sincronizadas, subagentes con `description` y skills existentes, specs con `Flujo enunciado:`.
- `scripts/validate_workflows.py --estricto` comprueba además `"active": false` y el nombre `NNN-slug.json` (sin `--estricto` se comporta como antes, para no cambiar la CI actual).
- Para añadir una skill externa nueva: copiarla a `.claude/skills/<nombre>/`, poner la cabecera SCOPE y la nota de precedencia, revisarla contra `AGENTS.md` §3 y ejecutar `python scripts/sync_agents.py`.
