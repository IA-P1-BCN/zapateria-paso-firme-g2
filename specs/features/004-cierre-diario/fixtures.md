# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 004 · Cierre diario — Fixtures

Entradas = respuestas de la API (listas). Datos ficticios sin datos personales reales. Se prueban con *Pin Data* en los nodos HTTP Request `Pedir ventas del día` y `Pedir abonos del día`.

## F-004-1 Día normal (CA-1, CA-2, CA-4)

**Ventas (`GET /api/ventas?desde=2026-10-20&hasta=2026-10-20`):**
```json
[
  {"id": 1, "fecha": "2026-10-20", "concepto": "Crema calzado", "importe": 4.5, "forma_pago": "efectivo"},
  {"id": 2, "fecha": "2026-10-20", "concepto": "Sandalia", "importe": 39.9, "forma_pago": "tarjeta"}
]
```

**Abonos (`GET /api/abonos?desde=2026-10-20&hasta=2026-10-20`):**
```json
[
  {"id": 10, "apartado_id": 25, "fecha": "2026-10-20", "importe": 10.0, "forma_pago": "bizum"},
  {"id": 11, "apartado_id": 7, "fecha": "2026-10-20", "importe": 20.0, "forma_pago": "efectivo"}
]
```

**Resultado esperado:**
- `sinMovimientos`: `false`
- `num_movimientos`: `4` (`num_ventas`: `2`, `num_abonos`: `2`)

| Concepto | Efectivo | Tarjeta | Bizum | Total |
|---|---|---|---|---|
| Ventas | 4,50 € (`4.5`) | 39,90 € (`39.9`) | 0,00 € (`0`) | 44,40 € (`44.4`) |
| Abonos | 20,00 € (`20`) | 0,00 € (`0`) | 10,00 € (`10`) | 30,00 € (`30`) |
| **Total** | **24,50 €** (`24.5`) | **39,90 €** (`39.9`) | **10,00 €** (`10`) | **74,40 €** (`74.4`) |

## F-004-2 Día sin movimientos (CA-3)

**Ventas:** `[]` (con `Always Output Data` activo en n8n entrega `[{}]`)
**Abonos:** `[]` (con `Always Output Data` activo en n8n entrega `[{}]`)

**Resultado esperado:**
- El flujo no se detiene ni lanza error.
- `sinMovimientos`: `true`, `num_movimientos`: `0`, todos los importes a `0` (`0,00 €`).
- El resumen enviado a Marisa indica explícitamente «Hoy no hubo movimientos».

## F-004-3 Precisión en coma flotante (CA-5)

**Ventas:**
```json
[
  {"id": 1, "fecha": "2026-10-20", "concepto": "Cordones", "importe": 0.1, "forma_pago": "efectivo"},
  {"id": 2, "fecha": "2026-10-20", "concepto": "Bolsita", "importe": 0.2, "forma_pago": "efectivo"}
]
```
**Abonos:** `[]`

**Resultado esperado:**
- Los sumandos no se alteran; el total en efectivo y el total general se redondean a 2 decimales: `0.3` (`0,30 €`), nunca `0.30000000000000004`.
