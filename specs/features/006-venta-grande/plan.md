## Visión general
- **Objetivo:** Detectar ventas cuyo importe supera **500 €** y notificar a Marisa por Gmail.
- **Umbral configurable:** 500 € (valor por defecto del briefing). 
- **Canal de notificación:** Gmail (credencial `Gmail tienda`).
- **Disparadores:**
  1. **Schedule Trigger** cada 15 min (`cron "*/15 * * * *"`) zona `Europe/Madrid`.
  2. **Webhook Trigger** `venta.registrada` (opcional, para cobertura completa).
- **Persistencia:** Data Table `avisos_ventas_grandes` (`venta_id`, `umbral`, `fecha_aviso`).
- **Manejo de errores:** Redirigir a Error Workflow `[005]` en caso de fallos de la API.

## Pasos del flujo
1. **Obtener ventas (schedule)** → `GET /api/ventas?desde=HOY&hasta=HOY`.
2. **Filtrar ventas > umbral** (`{{ $json.filter(v => v.importe > 500) }}`).
3. **Consultar Data Table** para evitar duplicados (`find` por `venta_id` y `fecha`).
4. **IF** → si ya notificado, descartar; si no, enviar email.
5. **Email Send** → plantilla `venta_grande.html` con datos de la venta.
6. **Data Table – Insert** registro del aviso.
7. **Webhook alternativa** (si llega evento `venta.registrada`): mismo proceso a partir del payload.
8. **Error Trigger** → redirige a `[005]` para errores 401/404/422.

## Variables configurables en n8n
- `umbral = 500`
- `zona_horaria = "Europe/Madrid"`
- `tabla_avisos = "avisos_ventas_grandes"`
- `cron = "*/15 * * * *"`

## Checklist de aprobación
- [ ] Plan revisado y aprobado.
- [ ] Data Table creada en n8n con columnas `venta_id`, `umbral`, `fecha_aviso`.
- [ ] Plantilla de email `venta_grande.html` disponible.
- [ ] Endpoint `GET /api/ventas` accesible y devuelve `id`, `cliente`, `email`, `producto`, `talla`, `importe`, `fecha`.
- [ ] Error Workflow `[005]` configurado.
