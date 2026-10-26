# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 004 · Cierre diario — Fixtures

Entradas = respuestas de la API (listas). Datos ficticios. Pinned data en los nodos HTTP Request.

## F-004-1 Día normal

Ventas:
```json
[{"id": 1, "fecha": "2026-10-20", "concepto": "Crema calzado", "importe": 4.5, "forma_pago": "efectivo"},
 {"id": 2, "fecha": "2026-10-20", "concepto": "Sandalia", "importe": 39.9, "forma_pago": "tarjeta"}]
```
Abonos:
```json
[{"id": 10, "apartado_id": 25, "fecha": "2026-10-20", "importe": 10.0, "forma_pago": "bizum"},
 {"id": 11, "apartado_id": 7, "fecha": "2026-10-20", "importe": 20.0, "forma_pago": "efectivo"}]
```
Esperado:

| | Efectivo | Tarjeta | Bizum | Total |
|---|---|---|---|---|
| Ventas | 4,50 | 39,90 | 0,00 | 44,40 |
| Abonos | 20,00 | 0,00 | 10,00 | 30,00 |
| **Total** | 24,50 | 39,90 | 10,00 | **74,40** |

## F-004-2 Día sin movimientos

Ventas `[]`, abonos `[]` → mensaje «Hoy no hubo movimientos», todo a 0,00, sin error.

## F-004-3 Decimales

Ventas con `0.1` y `0.2` en efectivo → total `0,30` (no `0,30000000000000004`).
