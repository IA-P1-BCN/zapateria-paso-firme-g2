---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
# GENERADO por scripts/sync_agents.py desde .agents/commands/paso-firme-review.md. No editar a mano.
description: Revisa un diff de Paso Firme contra las reglas de negocio del briefing
---

Aplica las instrucciones de la skill `paso-firme-review` (fuente: `.claude/skills/paso-firme-review/SKILL.md`).
Alcance indicado por la persona: $ARGUMENTS
Si no hay argumentos, revisa los cambios de la rama actual frente a `develop`.
