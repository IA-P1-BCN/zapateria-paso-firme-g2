---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
# GENERADO por scripts/sync_agents.py desde .agents/commands/revisar-flujo.md. No editar a mano.
description: Revisa un flujo antes de la PR (flow-reviewer + api-contract-checker)
---

Revisa el flujo de la feature **$ARGUMENTS** (número o ruta del JSON) antes de abrir la PR.

1. Lanza el subagente `flow-reviewer` sobre el flujo, su spec y sus fixtures.
2. Lanza el subagente `api-contract-checker` sobre el mismo JSON.
3. Junta ambos informes en uno: veredicto final (APROBADO solo si los dos lo están), bloqueantes, mejoras y cobertura de criterios de aceptación.
4. Prepara un borrador de descripción de PR usando la plantilla `.github/PULL_REQUEST_TEMPLATE.md` (no abras la PR).

No modifiques archivos.
