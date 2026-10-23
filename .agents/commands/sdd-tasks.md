# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

Descompón en tareas la feature **$ARGUMENTS** (número, p. ej. `003`).

1. Requisitos: `spec.md` `Aprobada` y `plan.md` existente. Si no, para y dilo.
2. Usa `specs/_templates/tasks.md` y la skill `sdd-workflow`.
3. Tareas atómicas (una sesión), con tipo `agente`/`humano`, agente sugerido, responsable `<<PENDIENTE>>`, dependencias y «hecho cuando» comprobable.
4. Todo lo que requiere la UI de n8n, credenciales o decisiones es `humano`. La última tarea es la bitácora.
5. Propón un reparto entre las 3 personas del equipo (ver `.agents/team.md`) que evite que dos editen el mismo JSON a la vez.

Escribe solo `specs/features/$ARGUMENTS-*/tasks.md`.
