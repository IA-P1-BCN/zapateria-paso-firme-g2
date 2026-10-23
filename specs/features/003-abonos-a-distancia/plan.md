# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 003 · Abonos a distancia — Plan

- **Estado del plan:** Borrador (no se construye hasta que la spec esté `Aprobada`)
- **Flujo n8n:** `[003] Abonos a distancia` → `automation/003-abonos-a-distancia.json` <<PENDIENTE: confirmar carpeta>>

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Recibir correo del banco` | <<PENDIENTE: Gmail Trigger / IMAP>> (+ Form Trigger en desarrollo) | |
| 2 | `Extraer datos del pago (IA)` | Basic LLM Chain / Information Extractor con salida estructurada | Devuelve `{es_pago, tipo, ordenante, importe, concepto}`. Solo extrae |
| 3 | `Validar extracción` | Code | `importe` número > 0, `es_pago` booleano; si no → dudoso |
| 4 | `¿Es un pago?` | IF | No → fin (ignorar) |
| 5 | `Pedir apartados activos` | HTTP Request `GET http://tienda:8000/api/apartados?estado=activo` | Credencial Header Auth |
| 6 | `Buscar candidatos` | Code | 1) nº en el concepto (`apartado 2`, `#2`) → ese id; 2) si no, nombre normalizado (sin tildes, mayúsculas, por palabras) contra `cliente`. Devuelve `candidatos[]` y `motivo` |
| 7 | `¿Cuántos candidatos?` | Switch | 0 → desconocido · 1 → seguir · >1 → dudoso. Ordenante con solo apellido+inicial y sin concepto → dudoso |
| 8 | `¿Se puede abonar?` | IF | Comprobación previa con datos de la app: `importe ≤ pendiente` y hoy ≤ `fecha_limite`. No sustituye a la app: es para dar un motivo claro |
| 9 | `¿Es transferencia?` | IF | Hasta decidir la forma de pago → preguntar a Marisa |
| 10 | `Registrar abono en la app` | HTTP Request `POST /api/apartados/{id}/abonos` `{importe, forma_pago: "bizum"}` · On Error → Continue (error output) | |
| 11 | `Preguntar a Marisa` | <<PENDIENTE: canal>> | Ordenante, importe, concepto, candidatos y motivo |
| 12 | `Avisar a Marisa: no se pudo registrar` | <<PENDIENTE: canal>> | `detail` del 422 o motivo de la comprobación previa |

## 2. Llamadas a la API de la tienda

| Método y ruta | Cuándo | Cuerpo / parámetros | Campos de respuesta que se usan |
|---|---|---|---|
| `GET /api/apartados` | Siempre que es pago | `estado=activo` (sin `pagina` → lista completa) | `id`, `cliente`, `pendiente`, `fecha_limite`, `estado` |
| `POST /api/apartados/{id}/abonos` | Un único candidato válido | `importe`, `forma_pago` | Respuesta `ApartadoOut`; errores 404/422 con `detail` |

## 3. Credenciales y variables (solo nombres)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| `API tienda` <<PENDIENTE>> | Header Auth | API |
| <<PENDIENTE>> | Gmail OAuth2 / IMAP | Leer el buzón |
| <<PENDIENTE>> | Credencial del proveedor de IA gratuito | Extracción |
| <<PENDIENTE>> | Correo / Telegram | Avisos a Marisa |

## 4. Manejo de errores

- Error Workflow `[ERR] Avisos de error`.
- `POST abonos` con salida de error: 422 → aviso a Marisa (no es un fallo del flujo).
- Fallo del modelo de IA: Retry On Fail 2 veces; si sigue fallando → preguntar a Marisa.

## 5. Datos de prueba

`fixtures.md`: los 9 correos de `data/correos/`, enviados por el Form Trigger. Antes de probar, **reiniciar los datos** (`docker compose down -v && docker compose up -d`), porque los de ejemplo son relativos al día de arranque.

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Casar nombres en un Code con normalización | `GET ?q=ordenante` | `q` hace `LIKE` y no ignora tildes ni apellidos extra («LUCIA GOMEZ PEREZ» no encuentra «Lucía Gómez») |
| No enviar la lista de apartados a la IA | IA que elige el apartado | Constitución II y IX |
