# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# Equipo y forma de trabajo

El enunciado está pensado para parejas; este equipo es de **3 personas**. Ajuste: roles que rotan por feature para que siempre haya alguien que revisa lo que otro construyó.

## Personas

| Persona | GitHub | Herramienta de IA | Modelo(s) | Nivel de acceso a n8n |
|---|---|---|---|---|
| <<PENDIENTE: nombre 1>> | <<PENDIENTE>> | <<PENDIENTE: OpenCode / Claude Code / otra>> | <<PENDIENTE>> | Instancia local propia |
| <<PENDIENTE: nombre 2>> | <<PENDIENTE>> | <<PENDIENTE>> | <<PENDIENTE>> | Instancia local propia |
| <<PENDIENTE: nombre 3>> | <<PENDIENTE>> | <<PENDIENTE>> | <<PENDIENTE>> | Instancia local propia |

Quien use una IA de pago lo indica aquí y limita su alcance a sus features asignadas (lo pide el enunciado).

## Roles por feature

| Rol | Responsabilidad |
|---|---|
| **Dueño/a de la spec** | Redacta (con `spec-writer`) y defiende la spec; resuelve los `<<PENDIENTE>>` |
| **Constructor/a** | Plan, tareas, flujo (con `flow-builder`), pruebas en su n8n |
| **Revisor/a** | Aprueba la spec, pasa `/revisar-flujo` y revisa la PR. Nunca es quien construyó |

## Reparto propuesto del nivel esencial (rotando roles)

| Feature | Spec | Construye | Revisa |
|---|---|---|---|
| 000 Enrutador + 005 Error Workflow | P1 | P2 | P3 |
| 001 Confirmación + 002 Recibo | P2 | P3 | P1 |
| 003 Abonos a distancia | P3 | P1 | P2 |
| 004 Cierre diario | P1 | P2 | P3 |

`<<PENDIENTE: confirmar reparto en el Kanban>>`

## Reglas de colaboración

- **Una feature = una rama = una PR**: `feature/HU-XX-slug`. Nadie edita el JSON de una feature que no tiene asignada.
- El enrutador `000` es compartido: cambios en él, en PR aparte y avisando al equipo.
- Cada persona trabaja contra **su** n8n local; lo compartido es el JSON en Git.
- Commits pequeños en español, en imperativo («Añade flujo de recibo de abono»). Los hace una persona, no el agente.
- PR a `develop` con al menos una aprobación de otra persona.
- Cambios en `.agents/`, `.claude/`, `.opencode/`, `scripts/` o `specs/constitution.md`: PR propia, revisada por el equipo.
