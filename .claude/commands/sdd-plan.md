---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
# GENERADO por scripts/sync_agents.py desde .agents/commands/sdd-plan.md. No editar a mano.
description: Escribe el plan técnico de una feature con spec aprobada y lo valida contra la API
argument-hint: "<NNN>"
---

Escribe el plan técnico de la feature **$ARGUMENTS** (número, p. ej. `003`).

1. Abre `specs/features/$ARGUMENTS-*/spec.md`. Si su `Estado:` no es `Aprobada`, **para** y dime qué falta.
2. Carga las skills `sdd-workflow`, `n8n-convenciones`, `tienda-api` y `dominio-apartados`.
3. Escribe `plan.md` desde `specs/_templates/plan.md`: nodos en orden, llamadas a la API, credenciales (solo nombres), errores, datos de prueba y decisiones.
4. Pasa el plan al subagente `api-contract-checker` y corrige lo que marque como roto. Anota en el plan el resultado.
5. Resume: nodos, endpoints, credenciales necesarias y `<<PENDIENTE>>`.

No generes JSON de flujos ni toques nada fuera de `specs/`.
