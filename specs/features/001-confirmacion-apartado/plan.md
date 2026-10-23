# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 001 · Confirmación de apartado — Plan

- **Estado del plan:** Borrador (no se construye hasta que la spec esté `Aprobada`)
- **Flujo n8n:** `[001] Confirmación de apartado` → `automation/001-confirmacion-apartado.json` <<PENDIENTE: confirmar carpeta>>

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Recibir apartado creado` | Execute Workflow Trigger | Entrada desde `[000]` con `datos` |
| 2 | `Formatear importes y fechas` | Set (o Code pequeño) | `79.9 → "79,90 €"`, `2027-01-18 → "18/01/2027"`; no cambia valores |
| 3 | `¿Tiene correo?` | IF (`email` no vacío) | |
| 4a | `Enviar confirmación al cliente` | <<PENDIENTE: Gmail / Send Email / Telegram>> | Plantilla con los campos de la spec |
| 4b | `Avisar a la tienda: sin correo` | <<PENDIENTE: canal tienda>> | Nº apartado + nombre |

## 2. Llamadas a la API de la tienda

Ninguna: el evento trae todo lo necesario.

## 3. Credenciales y variables (solo nombres)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| <<PENDIENTE: p. ej. `Correo tienda`>> | Gmail OAuth2 / SMTP | Enviar al cliente |
| <<PENDIENTE: p. ej. `Telegram tienda`>> | Telegram API | Avisar a Marisa |

## 4. Manejo de errores

- Error Workflow: `[ERR] Avisos de error`.
- Nodo de envío: reintento 2 veces (Settings → Retry On Fail).

## 5. Datos de prueba

`fixtures.md`: con correo, sin correo, sin talla, liquidado desde el alta.

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Formatear en Set con expresiones | Code | Menos código que revisar; Code solo si el formato se complica |
