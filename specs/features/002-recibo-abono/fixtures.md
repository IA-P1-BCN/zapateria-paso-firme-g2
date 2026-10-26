# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 002 · Recibo de abono — Fixtures

Entrada = `datos` del evento `abono.registrado`. Datos ficticios.

| Caso | Entrada (cambios sobre la base) | Resultado esperado |
|---|---|---|
| F-002-1 Recibo | Base | Recibo: pagado «20,00 €», abonado «30,00 €», pendiente «59,90 €», límite «18/01/2027» |
| F-002-2 Liquida | `"abonado": 89.9, "pendiente": 0.0, "estado": "liquidado", "importe": 59.9` | Aviso de recogida, no recibo |
| F-002-3 Sin correo | `"email": null` | Aviso a la tienda; ejecución sin error |

**Base**
```json
{"id": 25, "fecha": "2026-10-20", "cliente": "Carmen Ruiz", "telefono": "612 345 001", "email": "carmen@example.com", "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2027-01-18", "estado": "activo", "abonado": 30.0, "pendiente": 59.9, "importe": 20.0}
```
