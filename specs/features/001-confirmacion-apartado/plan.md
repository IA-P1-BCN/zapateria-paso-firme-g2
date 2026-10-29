# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 001 · Confirmación de apartado — Plan

- **Estado del plan:** Aprobado
- **Flujo n8n:** `[001] Confirmación de apartado` → `workflows/001-confirmacion-apartado.json`

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Recibir apartado creado` | Execute Workflow Trigger | Entrada desde `[000]` con `datos` |
| 2 | `Formatear importes y fechas` | Set (o Code pequeño) | `79.9 → "79,90 €"`, `2027-01-18 → "18/01/2027"`; no cambia valores |
| 3 | `¿Tiene correo?` | IF (`email` no vacío) | |
| 4a | `Enviar confirmación al cliente` | Gmail (operación *Send*) | Plantilla con los campos de la spec |
| 4b | `Avisar a la tienda: sin correo` | Gmail (*Send*), misma credencial | Nº apartado + nombre |

## 2. Llamadas a la API de la tienda

Ninguna: el evento trae todo lo necesario.

## 3. Credenciales y variables (solo nombres)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| `Gmail tienda` | Gmail OAuth2 | Enviar al cliente y avisar a la tienda |

Una sola credencial: el aviso de «sin correo» sale de la misma cuenta que la confirmación (ADR-0002, D12). No hay Telegram en esta feature.

## 4. Manejo de errores

- Error Workflow: `[ERR] Avisos de error`.
- Nodo de envío: reintento 2 veces (Settings → Retry On Fail).

## 5. Datos de prueba

`fixtures.md`: con correo, sin correo, sin talla, liquidado desde el alta.

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Formatear en Set con expresiones | Code | Menos código que revisar; Code solo si el formato se complica |
