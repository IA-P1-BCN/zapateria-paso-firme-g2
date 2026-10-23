---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
# GENERADO por scripts/sync_agents.py desde .agents/commands/sdd-spec.md. No editar a mano.
description: Redacta la spec SDD de una historia de usuario (delegando en spec-writer)
argument-hint: "<HU-XX | NNN | descripción>"
---

Redacta la spec SDD para: **$ARGUMENTS** (una HU como `HU-03`, un número de feature o una descripción).

Usa el subagente `spec-writer`. Pídele que:
1. Localice la HU en `docs/BRIEFING_zapateria.md` y el número de feature en `specs/backlog.md` (si no hay carpeta, que la cree desde `specs/_templates/`).
2. Escriba `specs/features/NNN-slug/spec.md` en estado `Borrador`.
3. Devuelva la ruta, los criterios de aceptación y los `<<PENDIENTE>>`.

Después, muéstrame el resumen y la lista de decisiones que tengo que tomar antes de aprobarla. No escribas plan ni tareas.
