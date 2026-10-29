# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 005 · Avisos de error — Plan

- **Estado del plan:** Borrador (no se construye hasta que la spec esté `Aprobada` → **Aprobada el 2026-10-29**)
- **Flujo n8n:** `[ERR] Avisos de error` → `workflows/005-error-workflow.json`

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Cuando falla un flujo` | Error Trigger | Capta el error del flujo que lo tenga asignado |
| 2 | `Preparar aviso sin datos` | Code | Toma `workflow.name`, `execution.lastNodeExecuted`, `execution.error.message`, `execution.url`; enmascara claves/secrets (`X-API-Key`, `Bearer`, `password`…) **y datos personales** (email, teléfono — decisión RGPD de la spec §9, F-005-4) |
| 3 | `Avisar a la tienda` | Gmail (Send) | Con credencial `Gmail tienda` (la misma del flujo 001, no hay nueva); Retry On Fail |

## 2. Llamadas a la API de la tienda

Ninguna.

## 3. Credenciales y variables (solo nombres)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| `Gmail tienda` | Gmail OAuth2 | Aviso a la tienda (reutilizada del flujo 001; sin credencial nueva) |

El destinatario del aviso es la cuenta de la tienda (coherente con la variable `correo_tienda` del flujo 001; su valor real es `<<PENDIENTE>>`, lo fija Levi).

## 4. Manejo de errores

Este flujo **no** se asigna a sí mismo como Error Workflow.

## 5. Datos de prueba

`fixtures.md` (F-005-1 … F-005-6): flujos `[TEST]` locales que fallan a propósito — error simple, secreto en el mensaje, API parada, datos personales en el error, fallo del propio aviso y errores seguidos. Los `[TEST]` no se exportan al repositorio. Cobertura: CA-1 → F-005-1/F-005-3 · CA-2 → F-005-2/F-005-4 · CA-3 es revisión de repo («flow-reviewer»), no fixture.

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Enmascarar en Code | Confiar en que los errores no traen secretos/datos | Los errores HTTP pueden incluir cabeceras; y spec §9 obliga a no enviar datos personales (RGPD, mínimo imprescindible) |
| Reutilizar credencial `Gmail tienda` | Crear una segunda credencial | Menos mantenimiento; el correo de tienda ya deja de ser `<<PENDIENTE>>` para el flujo 001 |
| Sin agrupación de avisos | Agrupar errores repetidos en ventanas de tiempo | Fuera del nivel esencial (spec §7/§10); se deja a nivel medio |
| Sin Error Workflows encadenados | Respaldo por otro canal si falla el propio aviso | n8n no encadena Error Workflows; el fallo queda visible en *Executions* (propuesta de nivel medio en spec §11) |
