# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 004 · Cierre diario — Plan

- **Spec:** `spec.md` (`Aprobada`)
- **Estado del plan:** Aprobado
- **Flujo n8n:** `[004] Cierre diario` → `workflows/004-cierre-diario.json`
- **Fecha:** 2026-10-28

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Cada noche` | Schedule Trigger (`n8n-nodes-base.scheduleTrigger`) | Dispara el flujo todos los días a las 21:30 (`Europe/Madrid`) |
| 2 | `Fecha de hoy` | Edit Fields / Set (`n8n-nodes-base.set`) | Calcula `fecha` = `{{ $now.setZone('Europe/Madrid').toFormat('yyyy-MM-dd') }}` |
| 3 | `Pedir ventas del día` | HTTP Request (`n8n-nodes-base.httpRequest`) | `GET http://tienda:8000/api/ventas?desde={{ $json.fecha }}&hasta={{ $json.fecha }}` con credencial `API tienda` y `alwaysOutputData: true` |
| 4 | `Pedir abonos del día` | HTTP Request (`n8n-nodes-base.httpRequest`) | `GET http://tienda:8000/api/abonos?desde={{ $('Fecha de hoy').first().json.fecha }}&hasta={{ $('Fecha de hoy').first().json.fecha }}` con credencial `API tienda` y `alwaysOutputData: true` |
| 5 | `Sumar por forma de pago` | Code (`n8n-nodes-base.code`) | Agrega importes por `efectivo`, `tarjeta` y `bizum` para ventas y abonos, calcula `sinMovimientos`, `num_movimientos`, redondea solo los totales a 2 decimales (`Math.round(total * 100) / 100`) y prepara el asunto y cuerpo del correo |
| 6 | `Guardar cierre en Google Sheets` | Google Sheets (`n8n-nodes-base.googleSheets`) | `appendOrUpdate` (upsert por columna `fecha`) en la hoja `Cierres` |
| 7 | `Enviar resumen a Marisa` | Gmail (`n8n-nodes-base.gmail`) | Envía el correo con el resumen diario (o el aviso «Hoy no hubo movimientos» si `sinMovimientos` es `true`) |

## 2. Llamadas a la API de la tienda

| Método y ruta | Cuándo | Parámetros | Campos de respuesta que se usan |
|---|---|---|---|
| `GET /api/ventas` | Cada noche tras calcular `fecha` | `desde`, `hasta` (`AAAA-MM-DD`, incluidas; sin `pagina`) | `id`, `importe`, `forma_pago` |
| `GET /api/abonos` | Tras consultar las ventas del día | `desde`, `hasta` (`AAAA-MM-DD`, incluidas; sin `pagina`) | `id`, `importe`, `forma_pago` |

Comprobado con `api-contract-checker`: Sí (2026-10-28).

## 3. Credenciales y variables (solo nombres, nunca valores)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| `API tienda` | Header Auth (`X-API-Key`) | Autenticación contra `http://tienda:8000/api/...` |
| `Google Sheets tienda` | Google Sheets OAuth2 API | Guardar histórico en la hoja `Cierres` |
| `Gmail tienda` | Gmail OAuth2 | Enviar el correo de resumen a Marisa |

## 4. Manejo de errores

- Error Workflow asignado en `settings.errorWorkflow`: `[ERR] Avisos de error`.
- `alwaysOutputData: true` en `Pedir ventas del día` y `Pedir abonos del día` para que una respuesta `[]` no detenga la ejecución.
- `retryOnFail: true` (`maxTries: 2`, `waitBetweenTries: 3000`) en los nodos HTTP Request, Google Sheets y Gmail.

## 5. Datos de prueba

Ver `fixtures.md` (casos `F-004-1` día normal, `F-004-2` día sin movimientos y `F-004-3` precisión decimal `0.1 + 0.2`).

## 6. Riesgos y decisiones

| Decisión | Alternativas descartadas | Por qué |
|---|---|---|
| Consultar la API (`GET /api/ventas` y `GET /api/abonos`) | Acumular eventos del webhook | Los avisos del webhook no tienen reintentos y pueden perderse |
| Redondear solo cada total resultante (`Math.round(total * 100) / 100`) | Redondear cada importe o no redondear | Constitución I y ADR-0002 D6 (evita `0.30000000000000004` sin tocar los importes de la app) |
| Upsert por `fecha` en Google Sheets | Append simple | Si el flujo se ejecuta dos veces el mismo día, actualiza la fila sin duplicar el cierre |
