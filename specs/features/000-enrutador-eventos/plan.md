# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 000 · Enrutador de eventos — Plan

- **Estado del plan:** Aprobado
- **Flujo n8n:** `[000] Enrutador de eventos` → `workflows/000-enrutador-eventos.json`

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Recibir evento de la tienda` | Webhook (POST, path `tienda`, Respond: Immediately) | Recibe el aviso |
| 2 | `¿Qué evento es?` | Switch (modo Rules sobre `{{ $json.body.evento }}`, fallback activado) | Reparte |
| 3a | `Confirmación pendiente` | No Op | Provisional; se sustituye por Execute Workflow → `[001]` en T-000-08 |
| 3b | `Recibo pendiente` | No Op | Provisional; se sustituye por Execute Workflow → `[002]` en T-000-08 |
| 3c | `Venta registrada (sin flujo aún)` | No Op | Hasta que exista `006` |
| 3d | `Apartado vencido (sin flujo aún)` | No Op | Hasta que exista `007` |
| 3e | `Evento desconocido` | No Op | Rama fallback |

Responder de inmediato evita que la app espere (la app corta a los 5 s).

## 2. Llamadas a la API de la tienda

Ninguna.

## 3. Credenciales y variables

Ninguna.

## 4. Manejo de errores

- Sin Error Workflow asignado todavía: se asignará `[ERR] Avisos de error` cuando exista `005` (T-000-08).
- En esta entrega no hay Execute Workflow; la decisión sobre «Wait for sub-workflow completion» se toma al cablear 001/002 en T-000-08.

## 5. Datos de prueba

`fixtures.md`: los 4 eventos reales + 3 casos fallback (evento desconocido, vacío y sin campo `evento`). Las pruebas manuales se envían a la **Test URL** (`/webhook-test/tienda`) con curl o con «Listen for test event»; CA-1 se comprueba desde la app con la **Production URL** (`/webhook/tienda`).

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Sub-flujos por evento | Todo en un flujo | Permite que 3 personas trabajen en paralelo sin pisar el mismo JSON |
