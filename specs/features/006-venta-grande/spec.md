# 006 · Aviso de ventas grandes — Spec

- **Estado:** Borrador
- **HU:** HU-09 · Aviso de ventas grandes (FL-04)
- **Flujo enunciado:** FL-04 · Venta grande
- **Nivel:** 🟡 Medio
- **Redacta:** BrianStiv · **Aprueba:** <<PENDIENTE>>
- **Fecha:** 2026-10-29

## 1. Objetivo
Detectar ventas cuyo importe supera un umbral configurable y notificar al responsable de la tienda (Marisa) para que revise la operación.

## 2. Historia de usuario
> Como **Marisa**, quiero recibir una notificación cada vez que se registre una venta cuyo importe sea superior a *X* €, para poder validar manualmente la operación y asegurarme de que el stock está disponible.

## 3. Disparador
| Tipo | Detalle |
|---|---|
| **Schedule Trigger** | Cada 15 min (cron `*/15 * * * *`) zona `Europe/Madrid` **o** (opcional) `Webhook` `venta.registrada` con payload de la venta. |

## 4. Entradas
| Campo | Origen | Obligatorio | Notas |
|---|---|---|---|
| `id` | evento / API | Sí | Identificador de la venta |
| `cliente` | evento / API | Sí | Nombre del cliente |
| `email` | evento / API | No | Si está disponible, se incluye en el mensaje |
| `producto`, `talla` | evento / API | Sí | Detalle del artículo vendido |
| `importe` | evento / API | Sí | Importe total de la venta (EUR) |
| `fecha` | evento / API | Sí | Fecha de la venta (`YYYY‑MM‑DD`) |

## 5. Salidas
| Salida | Destinatario | Canal | Contenido |
|---|---|---|---|
| Aviso de venta grande | Marisa | Gmail (credencial `Gmail tienda`) | Nº venta, cliente, producto, talla, importe, fecha |
| Registro de aviso | Data Table `avisos_ventas_grandes` | n8n Data Table | `venta_id`, `umbral`, `fecha_aviso` |
| Error | Error Workflow `[005]` | n8n Error Trigger | Detalle del error de la API |

## 6. Reglas de negocio aplicables
- **R‑09**: Toda venta > *umbral* debe ser revisada manualmente.
- **Constitución I**: Los importes se usan tal cual, sin redondeos intermedios.

## 7. Casos de borde y errores
| Caso | Comportamiento esperado |
|---|---|
| Importe ≤ umbral | No se envía aviso, el flujo termina normalmente. |
| Importe > umbral pero `email` ausente | El aviso se envía sin incluir el email del cliente. |
| API no responde | Reintentos (2) y, si sigue fallando, redirigir a Error Workflow `[005]`. |
| Aviso ya enviado para la misma venta | Consultar Data Table `avisos_ventas_grandes`; si existe registro con `venta_id` y fecha de hoy, no volver a enviar. |

## 8. Criterios de aceptación
- [ ] CA‑1 El flujo se ejecuta cada 15 min y detecta ventas > *umbral*.
- [ ] CA‑2 Se envía un email a Marisa con todos los datos de la venta.
- [ ] CA‑3 No se envían avisos duplicados para la misma venta en el mismo día.
- [ ] CA‑4 En caso de error de la API, el flujo redirige a `[005] Error Workflow`.
- [ ] CA‑5 Los registros de avisos se guardan en la Data Table `avisos_ventas_grandes` con columnas `venta_id`, `umbral`, `fecha_aviso`.

## 9. Datos personales
- Nombre y email del cliente (solo se usan para incluir en el cuerpo del email; no se almacenan fuera del flujo). No se envían a terceros ni a modelos de IA.

## 10. Fuera de alcance
- Generación automática de tickets en el sistema de tickets interno.
- Integración con sistemas de pago externos.

## 11. Preguntas abiertas
- <<PENDIENTE: Confirmar umbral exacto (ej. 500 €).>>
- <<PENDIENTE: Elegir canal de notificación final (email vs Slack).>>
- <<PENDIENTE: Decidir si usar Schedule o Webhook como disparador principal.>>
