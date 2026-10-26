# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# Equipo y forma de trabajo

El enunciado está pensado para parejas; este equipo es de **3 personas**. Ajuste: roles que rotan por feature para que siempre haya alguien que revisa lo que otro construyó.

## Personas

| Persona | GitHub | Herramienta de IA | Modelo(s) | Nivel de acceso a n8n |
|---|---|---|---|---|
| Levi Flores | `levifvy` | <<PENDIENTE: OpenCode / Claude Code / otra>> | <<PENDIENTE>> | Instancia local propia |
| Brian Hañari | `BrianStiv` | <<PENDIENTE: OpenCode / Claude Code / otra>> | <<PENDIENTE>> | Instancia local propia |
| Miguel Matesanz | `mmatesanzg23` | <<PENDIENTE: OpenCode / Claude Code / otra>> | <<PENDIENTE>> | Instancia local propia |

Quien use una IA de pago lo indica aquí y limita su alcance a sus features asignadas (lo pide el enunciado).
Herramienta y modelo quedan pendientes: los rellena cada persona (un agente no los supone).

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

`<<PENDIENTE: confirmar reparto en el Kanban y a qué persona corresponden P1, P2 y P3>>`

## Daily Scrum

La ceremonia diaria del equipo. No es una feature ni un flujo de n8n: sirve para mover el tablero, desbloquear y
decidir el siguiente paso. Detalle completo en [`docs/dailies/README.md`](../docs/dailies/README.md).

| Qué | Cómo |
|---|---|
| Cuándo | Lunes a viernes, 15 min (referencia: 09:00 `Europe/Madrid`) |
| Tarjeta | Una por **equipo y día**: `[Daily] AAAA-MM-DD`, etiquetas `daily` + `scrum`, asignada a las tres personas |
| Creación | Automática con `.github/workflows/daily-scrum.yml` (cron `30 6 * * 1-5`) |
| Facilitador/a | Rota por semana: **Levi → Brian → Miguel**, ancla `2026-10-26` |
| Tablero | Mismo Project, vista `Dailies`; columnas del campo `Estado daily`: `Inicio` → `¿Ha pasado algo?` → `Cierre` |
| Movimiento | `Inicio` automático (valor por defecto); `¿Ha pasado algo?` y `Cierre` **a mano** |
| Historial | Tabla `Historial de la daily` en el cuerpo del issue + vista `Historial de dailys` |

- Las vistas `tablero`, `por historia` y `se puede empezar` no cambian.
- Las tareas y PRs se mueven solas con `Status`; las dailys se arrastran a mano con `Estado daily`.
- Un bloqueo detectado en la daily se convierte en issue con etiqueta `bloqueado` y responsable; si no, no existe.

## Reglas de colaboración

- **Una feature = una rama = una PR**: `feature/HU-XX-slug`. Nadie edita el JSON de una feature que no tiene asignada.
- El enrutador `000` es compartido: cambios en él, en PR aparte y avisando al equipo.
- Cada persona trabaja contra **su** n8n local; lo compartido es el JSON en Git.
- Commits pequeños en español, en imperativo («Añade flujo de recibo de abono»). Los hace una persona, no el agente.
- PR a `develop` con al menos una aprobación de otra persona.
- Cambios en `.agents/`, `.claude/`, `.opencode/`, `scripts/` o `specs/constitution.md`: PR propia, revisada por el equipo.
