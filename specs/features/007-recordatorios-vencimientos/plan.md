# 007 · Recordatorios y Vencimientos — Plan

## Visión General
- **Objetivo:** Implementar un flujo n8n que, cada mañana a las **06:00 CET** (Barcelona), envíe recordatorios de pagos pendientes (HU‑06) y gestione los vencimientos de apartados (HU‑07).
- **Persistencia:** Utilizar una **Data Table** (`avisos_enviados`) para registrar qué avisos ya fueron enviados y evitar duplicados.
- **Triggers:** `Schedule Trigger` (06:00 CET) → `GET /api/apartados?estado=activo&fecha_limite<=HOY`.
- **Salidas:** Emails a clientes y actualización del estado del apartado a `vencido` cuando corresponde.

## Pasos del Flujo
1. **Obtener Apartados Activos con Fecha Límite ≤ Hoy**
   - *API:* `GET /api/apartados?estado=activo&fecha_limite={{ $now.format('YYYY-MM-DD') }}`
2. **Filtrar Según Estado**
   - Si `pendiente > 0` → **Recordatorio** (HU‑06).
   - Si `pendiente == 0` → **Vencimiento** (HU‑07).
3. **Consultar Data Table `avisos_enviados`**
   - Evitar reenviar avisos para el mismo apartado en la misma fecha.
4. **Enviar Email**
   - Plantilla diferente para recordatorio y vencimiento.
5. **Actualizar Data Table**
   - Insertar registro `{ apartado_id, tipo_avisos, fecha }`.
6. **Para Vencimientos:**
   - Llamar a `POST /api/apartados/{id}/vencer`.
   - Registrar vale generado por la app.
7. **Manejo de Errores**
   - En caso de error de API (`401`, `404`, `422`) redirigir a **Error Workflow** `[005]`.
8. **Fin del Flujo** – `No activar` en n8n (activo = false).

## Variables Configurables en n8n
- `hora_ejecucion = "06:00"`
- `zona_horaria = "Europe/Madrid"`
- `nombre_tabla = "avisos_enviados"`

## Requisitos de Seguridad y RGPD
- No se incluyen datos personales en la Data Table; solo IDs y timestamps.
- Los correos se generan con información mínima requerida (nombre del cliente, importe, fecha límite).

## Checklist de Aprobación
- [ ] Plan revisado y aprobado.
- [ ] Data Table creada en n8n con columnas `apartado_id`, `tipo`, `fecha`.
- [ ] Plantillas de email disponibles.
- [ ] Endpoint `POST /api/apartados/{id}/vencer` comprobado.
- [ ] Error Workflow `[005]` configurado para recibir errores.
