---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
# GENERADO por scripts/sync_agents.py desde .agents/commands/construir-flujo.md. No editar a mano.
description: Genera el JSON del flujo n8n de una feature (delegando en flow-builder)
---

Construye el flujo n8n de la feature **$ARGUMENTS** (número, y opcionalmente el id de tarea: `003 T-003-04`).

Usa el subagente `flow-builder`. Antes de nada, debe comprobar sus precondiciones (spec aprobada, plan y tareas). Si no se cumplen, que pare y me diga qué falta.

Cuando termine:
1. Enséñame el resumen: archivos, nodos, endpoints y credenciales que tengo que asignar a mano.
2. Recuérdame los pasos humanos: importar en n8n (skill `n8n-import-export`), asignar credenciales, probar con `fixtures.md`.
3. No actives el flujo, no hagas commit ni push.
