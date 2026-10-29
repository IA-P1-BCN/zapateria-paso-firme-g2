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

## Reparto confirmado (octubre 2026, en los issues de GitHub)

Regla del equipo: **cada persona hace su feature entera** (spec, flujo, pruebas y PR) y la
**revisa una de las otras dos** (nunca quien construyó). El revisor se añade como asignado
de la subtarea «PR y revisión humana» y en la de «Revisión de seguridad».

### Nivel esencial

| Feature | Hace entera | Revisa |
|---|---|---|
| 000 Enrutador de eventos | Miguel (`mmatesanzg23`) | Levi (`levifvy`) |
| 001 Confirmación al apartar | Brian (`BrianStiv`) | Miguel |
| 002 Recibo de abono *(cerrada; quedó sin asignación en GitHub)* | Miguel (cierre de la feature) | Levi |
| 003 Abonos a distancia | Levi (`levifvy`) | Brian (`BrianStiv`) |
| 004 Cierre diario | Miguel | Brian |
| 005 Error Workflow | Brian | Levi |

### Nivel medio

| Feature | Hace entera | Revisa |
|---|---|---|
| 006 Venta grande | Levi | Brian |
| 007 Recordatorios y vencimientos | Brian | Miguel |
| 008 Informe mensual | Miguel | Levi |
| 009 Migración del Excel | Levi | Miguel |
| 010 Sub: buscar apartado | Brian | Levi |
| 011 Sub: enviar notificación | Miguel | Brian |

### Nivel avanzado

| Feature | Hace entera | Revisa |
|---|---|---|
| 012 Asistente de Telegram para clientes | Levi | Brian |
| 013 Asistente de Telegram para Marisa | Brian | Miguel |
| 014 Entrada automática de datos | Miguel | Levi |
| 015 Datos personales *(transversal)* | Los tres (cada uno ajusta sus flujos; webhook: Brian) | Por flujo, el que no lo construyó |

Si 012 y 013 deciden compartir bot, 013 reutiliza la credencial de 012 (ya apuntado en `T-013-03`).
El reparto se confirma en la daily antes de empezar cada nivel; si salta un cambio, se ajusta aquí **y** en los issues.

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
