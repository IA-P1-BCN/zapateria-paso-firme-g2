# 007 · Recordatorios y Vencimientos — Tasks

## Tareas de desarrollo

| ID | Descripción | Responsabilidad | Dependencia |
|----|-------------|----------------|-------------|
| T1 | Crear Data Table `avisos_enviados` en n8n con columnas `apartado_id`, `tipo`, `fecha` | flow‑builder | — |
| T2 | Configurar **Schedule Trigger** a `06:00` CET (`Europe/Madrid`) | flow‑builder | — |
| T3 | Añadir nodo **HTTP Request**: `GET /api/apartados?estado=activo&fecha_limite={{ $now.format('YYYY-MM-DD') }}` | flow‑builder | T2 |
| T4 | Añadir nodo **Set** para separar resultados en `recordatorios` (pendiente > 0) y `vencimientos` (pendiente = 0) | flow‑builder | T3 |
| T5 | Añadir nodo **Data Table – Find** para buscar registros en `avisos_enviados` y filtrar por `apartado_id` y `fecha` = hoy | flow‑builder | T4 |
| T6 | Añadir nodo **IF** para descartar ya enviados | flow‑builder | T5 |
| T7 | **Email → Recordatorio**: usar plantilla *recordatorio.html* con datos del cliente y importe pendiente | flow‑builder | T6 |
| T8 | **Data Table – Insert**: registrar envío (`tipo: recordatorio`) | flow‑builder | T7 |
| T9 | **Email → Vencimiento**: usar plantilla *vencimiento.html* y enviar | flow‑builder | T6 |
| T10 | **HTTP Request**: `POST /api/apartados/{{ $json.id }}/vencer` para marcar como vencido y generar vale | flow‑builder | T9 |
| T11 | **Data Table – Insert**: registrar envío (`tipo: vencimiento`) | flow‑builder | T10 |
| T12 | **Error Handling**: nodo *Error Trigger* → **Error Workflow** `[005]` para códigos 401/404/422 | flow‑builder | T3,T9,T10 |
| T13 | Desactivar activación del flujo (`"active": false`) antes de exportar JSON | flow‑builder | — |

## Checklist de aceptación
- [ ] Todos los nodos creados conforme a la convención de nombres *Verbo + Objeto*.
- [ ] Data Table `avisos_enviados` contiene los registros esperados.
- [ ] Los correos llegan correctamente con la información mínima requerida.
- [ ] En caso de error, el flujo redirige a **[005] Error Workflow**.
- [ ] El JSON exportado está en `workflows/007-recordatorios-vencimientos.json` y tiene `"active": false`.
