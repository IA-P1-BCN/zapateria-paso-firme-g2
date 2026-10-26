# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# scripts/ · Utilidades de la capa de agentes

Python 3.10+ sin dependencias. No escriben en `backend/`, `frontend/` ni `workflows/` (`validate_workflows.py` solo lee los JSON).

| Script | Para qué |
|---|---|
| `sync_agents.py` | Genera `.claude/agents|commands` y `.opencode/agents|commands` desde `.agents/`, y copia `.claude/skills/` a `.opencode/skills/`. `--check` solo comprueba |
| `validate_agent_infra.py` | Valida skills, cabeceras SCOPE, sincronización y specs. `--alcance --base develop` además falla si la rama toca código de la app |
| `new_feature.py` | Crea `specs/features/NNN-slug/` desde las plantillas |

```bash
python scripts/sync_agents.py
python scripts/validate_agent_infra.py --alcance
python scripts/new_feature.py 006 venta-grande --hu HU-09 --titulo "Venta grande"
```
