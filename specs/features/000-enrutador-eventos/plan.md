# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 000 · Enrutador de eventos — Plan

- **Estado del plan:** Aprobado
- **Flujo n8n:** `[000] Enrutador de eventos` → `workflows/000-enrutador-eventos.json`

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Recibir evento de la tienda` | Webhook (POST, path `tienda`, Respond: Immediately) | Recibe el aviso |
| 2 | `¿Qué evento es?` | Switch (modo Rules sobre `{{ $json.body.evento }}`, fallback activado) | Reparte |
| 3a | `Extraer datos del apartado` → `Llamar a confirmación de apartado` | Code + Execute Workflow | Cableado a `[001]` (T-000-08) |
| 3b | `Extraer datos del abono` → `Llamar a recibo de abono` | Code + Execute Workflow | Cableado a `[002]` (T-000-08) |
| 3c | `Venta registrada (sin flujo aún)` | No Op | Hasta que exista `006` |
| 3d | `Apartado vencido (sin flujo aún)` | No Op | Hasta que exista `007` |
| 3e | `Evento desconocido` | No Op | Rama fallback |

Responder de inmediato evita que la app espere (la app corta a los 5 s).

## 2. Llamadas a la API de la tienda

Ninguna.

## 3. Credenciales y variables

Ninguna.

## 4. Manejo de errores

- Error Workflow asignado: `[ERR] Avisos de error` (005), tras existir el flujo (T-000-08).
- Los sub-flujos 001 y 002 se invocan con Execute Workflow (un sub-flujo por evento); se pasa el `datos` del webhook como entrada.

## 5. Datos de prueba

`fixtures.md`: los 4 eventos reales + 3 casos fallback (evento desconocido, vacío y sin campo `evento`). Las pruebas manuales se envían a la **Test URL** (`/webhook-test/tienda`) con curl o con «Listen for test event»; CA-1 se comprueba desde la app con la **Production URL** (`/webhook/tienda`).

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Sub-flujos por evento | Todo en un flujo | Permite que 3 personas trabajen en paralelo sin pisar el mismo JSON |
