# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 000 · Enrutador de eventos — Plan

- **Estado del plan:** Borrador (no se construye hasta que la spec esté `Aprobada`)
- **Flujo n8n:** `[000] Enrutador de eventos` → `workflows/000-enrutador-eventos.json`

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Recibir evento de la tienda` | Webhook (POST, path `tienda`, Respond: Immediately) | Recibe el aviso |
| 2 | `¿Qué evento es?` | Switch (modo Rules sobre `{{ $json.body.evento }}`, fallback activado) | Reparte |
| 3a | `Ir a confirmación de apartado` | Execute Workflow → `[001] Confirmación de apartado` | Pasa `body.datos` |
| 3b | `Ir a recibo de abono` | Execute Workflow → `[002] Recibo de abono` | Pasa `body.datos` |
| 3c | `Venta registrada (sin flujo aún)` | No Op | Hasta que exista `006` |
| 3d | `Apartado vencido (sin flujo aún)` | No Op | Hasta que exista `007` |
| 3e | `Evento desconocido` | No Op | Rama fallback |

Responder de inmediato evita que la app espere (la app corta a los 5 s).

## 2. Llamadas a la API de la tienda

Ninguna.

## 3. Credenciales y variables

Ninguna.

## 4. Manejo de errores

- Settings → Error Workflow: `[ERR] Avisos de error`.
- Execute Workflow con «Wait for sub-workflow completion» <<PENDIENTE: decidir; desactivado = el enrutador no se entera de fallos del hijo, que los avisa su propio Error Workflow>>.

## 5. Datos de prueba

`fixtures.md`: los 4 eventos reales + uno desconocido. Se envían a la **Test URL** (`/webhook-test/tienda`) con curl o con «Listen for test event».

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Sub-flujos por evento | Todo en un flujo | Permite que 3 personas trabajen en paralelo sin pisar el mismo JSON |
