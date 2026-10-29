# 006 · Aviso de ventas grandes — Tasks

## Tareas de desarrollo

| ID | Descripción | Responsabilidad | Dependencia |
|----|-------------|----------------|-------------|
| T1 | Crear Data Table `avisos_ventas_grandes` en n8n con columnas `venta_id`, `umbral`, `fecha_aviso` | flow‑builder | — |
| T2 | Configurar **Schedule Trigger** a `*/15 * * * *` zona `Europe/Madrid` | flow‑builder | — |
| T3 | Configurar **Webhook Trigger** `venta.registrada` (opcional) | flow‑builder | — |
| T4 | Añadir nodo **HTTP Request**: `GET /api/ventas?desde=HOY&hasta=HOY` (para schedule) | flow‑builder | T2 |
| T5 | Añadir nodo **Set** / **Function** para filtrar ventas con `importe > 500` | flow‑builder | T4 |
| T6 | Añadir nodo **Data Table – Find** para buscar registros en `avisos_ventas_grandes` (por `venta_id` y fecha) | flow‑builder | T5 |
| T7 | Añadir nodo **IF** para descartar ya enviados | flow‑builder | T6 |
| T8 | Añadir nodo **Email → Gmail** con plantilla `venta_grande.html` y datos de la venta | flow‑builder | T7 |
| T9 | Añadir nodo **Data Table – Insert**: registrar envío (`venta_id`, `umbral`, `fecha_aviso`) | flow‑builder | T8 |
| T10 | Repetir pasos 4‑9 para el **Webhook Trigger** (usar mismo sub‑flujo) | flow‑builder | T3 |
| T11 | Añadir nodo **Error Trigger** → Error Workflow `[005]` para códigos 401/404/422 | flow‑builder | T4, T8, T10 |
| T12 | Desactivar activación del flujo (`"active": false`) antes de exportar JSON | flow‑builder | — |

## Checklist de aceptación
- [ ] Data Table `avisos_ventas_grandes` creada y accesible.
- [ ] El flujo envía email solo cuando `importe > 500` y no se ha enviado antes ese día.
- [ ] En caso de error, el flujo redirige a `[005]`.
- [ ] El JSON exportado está en `workflows/006-venta-grande.json` con `"active": false`.
