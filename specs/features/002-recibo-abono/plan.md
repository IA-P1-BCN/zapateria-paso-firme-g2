# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 002 · Recibo de abono — Plan

- **Estado del plan:** Borrador (no se construye hasta que la spec esté `Aprobada`)
- **Flujo n8n:** `[002] Recibo de abono` → `workflows/002-recibo-abono.json`

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Recibir abono registrado` | Execute Workflow Trigger | Entrada desde `[000]` |
| 2 | `Formatear importes y fechas` | Set | Formato español, sin cambiar valores |
| 3 | `¿Tiene correo?` | IF | |
| 4 | `¿Liquidado?` | IF (`estado` = `liquidado`) | |
| 5a | `Enviar recibo al cliente` | Gmail (Send) | |
| 5b | `Enviar aviso de recogida` | Gmail (Send) | |
| 5c | `Avisar a la tienda: sin correo` | Gmail (Send) | |

Si se decide mostrar la forma de pago: nodo `Pedir apartado a la API` (HTTP Request `GET http://tienda:8000/api/apartados/{{id}}`, credencial `API tienda`) antes del paso 2.

## 2. Llamadas a la API de la tienda

| Método y ruta | Cuándo | Parámetros | Campos usados |
|---|---|---|---|
| `GET /api/apartados/{id}` | Solo si se muestra la forma de pago | — | `abonos[-1].forma_pago` |

## 3. Credenciales y variables (solo nombres)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| `API tienda` (ADR-0002, D5) | Header Auth (`X-API-Key`) | Solo si se llama a la API |
| <<PENDIENTE>> | Correo / Telegram | Envíos |

## 4. Manejo de errores

Error Workflow `[ERR] Avisos de error`; Retry On Fail en los envíos.

## 5. Datos de prueba

`fixtures.md`.

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Decidir por `estado` | Comprobar `pendiente == 0` | La app ya fija el estado; evita errores de redondeo |
