# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 000 · Enrutador de eventos — Fixtures

Payloads con la forma exacta que envía la app (`docs/guia-de-la-app.md` §6). Datos ficticios.
Enviar a la Test URL mientras se construye:

```bash
curl -X POST http://localhost:5678/webhook-test/tienda -H "Content-Type: application/json" -d '<payload>'
```

| Caso | Payload | Rama esperada |
|---|---|---|
| F-000-1 | `apartado.creado` (abajo) | Confirmación de apartado |
| F-000-2 | `abono.registrado` | Recibo de abono |
| F-000-3 | `venta.registrada` | No Op venta |
| F-000-4 | `apartado.vencido` | No Op vencido |
| F-000-5 | `{"evento": "otra.cosa", "datos": {}}` | Fallback, sin error |
| F-000-6 | `{"evento": "", "datos": {}}` | Fallback, sin error |
| F-000-7 | `{"datos": {}}` (sin `evento`) | Fallback, sin error |

**F-000-1**
```json
{"evento": "apartado.creado", "datos": {"id": 25, "fecha": "2026-10-20", "cliente": "Carmen Ruiz", "telefono": "612 345 001", "email": "carmen@example.com", "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2027-01-18", "estado": "activo", "abonado": 10.0, "pendiente": 79.9}}
```

**F-000-2**
```json
{"evento": "abono.registrado", "datos": {"id": 25, "fecha": "2026-10-20", "cliente": "Carmen Ruiz", "telefono": "612 345 001", "email": "carmen@example.com", "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2027-01-18", "estado": "activo", "abonado": 30.0, "pendiente": 59.9, "importe": 20.0}}
```

**F-000-3**
```json
{"evento": "venta.registrada", "datos": {"id": 257, "fecha": "2026-10-20", "concepto": "Crema calzado", "importe": 4.5, "forma_pago": "efectivo"}}
```

**F-000-4**
```json
{"evento": "apartado.vencido", "datos": {"apartado": {"id": 16, "cliente": "Paula Ramos", "email": "paula16@example.com", "producto": "Zapatilla running azul", "precio": 64.5, "abonado": 5.0, "pendiente": 59.5, "estado": "vencido"}, "vale": {"id": 2, "codigo": "VALE-00016", "apartado_id": 16, "fecha": "2026-10-20", "importe": 5.0, "usado": 0}}}
```

## Resultados de las pruebas (2026-10-27)

Pruebas manuales con la **Test URL** y prueba final desde la app con la **Production URL**:

| Caso | Ejecución | Modo | Producción | Último nodo | Resultado |
|---|---|---|---|---|---|
| F-000-1 | 2 | `manual` | No | `Confirmación pendiente` | OK |
| F-000-2 | 3 | `manual` | No | `Recibo pendiente` | OK |
| F-000-3 | 4 | `manual` | No | `Venta registrada (sin flujo aún)` | OK |
| F-000-4 | 5 | `manual` | No | `Apartado vencido (sin flujo aún)` | OK |
| F-000-5 | 6 | `manual` | No | `Evento desconocido` | OK |
| F-000-6 | 7 | `manual` | No | `Evento desconocido` | OK |
| F-000-7 | 8 | `manual` | No | `Evento desconocido` | OK |
| CA-1 (apartado #25) | 9 | `webhook` | Sí | `Confirmación pendiente` | OK |

La ejecución 1 no se usa como evidencia: fue una ejecución parcial del trigger (solo el nodo Webhook). Todas las ejecuciones de la tabla terminaron en `success`.

El flujo se desactivó después de CA-1; el JSON versionado permanece con `"active": false`.
