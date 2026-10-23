---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
# GENERADO por scripts/sync_agents.py desde .agents/commands/bitacora.md. No editar a mano.
description: Registra en docs/ai-log.md lo hecho con IA (delegando en ai-scribe)
argument-hint: "<feature, tarea o descripción>"
---

Registra en la bitácora de IA lo hecho en: **$ARGUMENTS** (feature, tarea o descripción breve).

Usa el subagente `ai-scribe`. Pásale: herramienta y modelo usados en esta sesión, prompts clave, errores o alucinaciones detectados y decisiones tomadas (aceptado / rechazado / modificado y por qué), con enlaces a la spec y la tarea.

Muéstrame la entrada añadida y los `<<PENDIENTE>>` que tengo que completar.
