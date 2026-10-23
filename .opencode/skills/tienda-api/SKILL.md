---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)
# GENERADO por scripts/sync_agents.py desde .claude/skills/tienda-api/SKILL.md. No editar a mano.
name: tienda-api
description: Contrato de la API REST de la tienda (endpoints, parámetros, cuerpos, respuestas, errores 401/404/422) y de los eventos del webhook hacia n8n. Úsala al diseñar o revisar cualquier nodo HTTP Request, Webhook o Switch de eventos, o al escribir fixtures con payloads.
---

# Contrato app ↔ n8n

**Fuente de verdad**: `backend/routes/*.py` (rutas), `backend/schemas/*.py` (forma de los datos), `backend/controllers/*.py` (qué evento se envía), `docs/guia-de-la-app.md`. Si algo de aquí no coincide con el código, manda el código: avisa en tu resumen.

## Direcciones

| Desde | App | n8n |
|---|---|---|
| Tu máquina | `http://localhost:8000` (Swagger en `/docs`) | `http://localhost:5678` |
| Dentro de n8n | `http://tienda:8000` | — |
| Dentro de la app | — | `http://n8n:5678` |

## Autenticación

Cabecera `X-API-Key` en todo `/api/...`. En n8n: credencial **Header Auth** (Name `X-API-Key`), nombre acordado `API tienda` <<PENDIENTE: confirmar>>. Sin clave → `401`.

## Endpoints

| Método y ruta | Entrada | Respuesta |
|---|---|---|
| `GET /api/apartados` | Query: `estado` (activo/liquidado/vencido), `q`, `pagina`, `por_pagina` | Lista `ApartadoOut`; total en cabecera `X-Total-Count`. Sin `pagina` → todo |
| `GET /api/apartados/resumen` | — | `{activo, liquidado, vencido, total}` |
| `GET /api/apartados/{id}` | — | `ApartadoOut` + `abonos[]` + `vale` (o `null`) |
| `POST /api/apartados` | `cliente`, `producto`, `precio`, `abono_inicial` · opc. `telefono`, `email`, `talla`, `forma_pago`, `fecha` | `ApartadoOut` (201) |
| `POST /api/apartados/{id}/abonos` | `importe` · opc. `forma_pago` (def. efectivo), `fecha` | `ApartadoOut` (201) |
| `POST /api/apartados/{id}/vencer` | Sin cuerpo | `{apartado, vale}` |
| `GET /api/abonos` | `desde`, `hasta` (AAAA-MM-DD, incluidas) | Lista `AbonoOut` |
| `GET /api/ventas` | `desde`, `hasta`, `orden` (asc/desc), `pagina`, `por_pagina` | Lista `VentaOut` |
| `POST /api/ventas` | `concepto`, `importe` · opc. `forma_pago`, `fecha` | `VentaOut` (201) |
| `GET /api/vales` | — | Lista `ValeOut` |
| `GET /api/excel` | — | Archivo Excel |

`fecha` en los POST es **solo para migrar** datos antiguos.

## Formas

- `ApartadoOut`: `id, fecha, cliente, telefono?, email?, producto, talla?, precio, fecha_limite, estado, abonado, pendiente`
- `AbonoOut`: `id, apartado_id, fecha, importe, forma_pago`
- `VentaOut`: `id, fecha, concepto, importe, forma_pago`
- `ValeOut`: `id, codigo, apartado_id, fecha, importe, usado`

## Errores

Siempre `{"detail": "..."}`: `401` clave, `404` no existe, `422` regla del negocio (mensaje legible para reenviar a Marisa). En n8n un 4xx detiene el flujo salvo *Settings → On Error → Continue (using error output)*.

## Webhook (app → n8n)

`POST http://n8n:5678/webhook/tienda` · cuerpo `{"evento", "datos"}` · en n8n se lee como `$json.body.*`.
Eventos y ejemplos completos: [webhook-eventos.md](webhook-eventos.md).

Recuerda: un aviso, sin reintentos, sin autenticación, después de responder a la dependienta (timeout 5 s). Test URL `/webhook-test/tienda` solo con «Listen for test event»; la app usa la Production URL (flujo publicado).

## No existe (no lo inventes)

Endpoints de clientes, productos, stock, cierres, recordatorios, consentimientos, ni para marcar un vale como usado.
