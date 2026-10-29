# 007 · Recordatorios y Vencimientos — Fixtures

## Payloads de ejemplo para pruebas

```json
{
  "apartado_id": 123,
  "cliente": "Juan Pérez",
  "email": "juan.perez@example.com",
  "telefono": "601234567",
  "fecha_limite": "2026-10-30",
  "pendiente": 45.50,
  "estado": "activo"
}
```

- **Recordatorio**: `pendiente > 0`
- **Vencimiento**: `pendiente == 0`

Utilizar estos datos para probar los nodos de **Email**, **Data Table** y la llamada `POST /api/apartados/{id}/vencer`.
