# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 004 · Cierre diario — Plan

- **Estado del plan:** Borrador (no se construye hasta que la spec esté `Aprobada`)
- **Flujo n8n:** `[004] Cierre diario` → `workflows/004-cierre-diario.json`


## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Cada noche` | Schedule Trigger | Hora en variable <<PENDIENTE>> |
| 2 | `Fecha de hoy` | Set | `{{ $now.toFormat('yyyy-MM-dd') }}` |
| 3 | `Pedir ventas del día` | HTTP Request GET `/api/ventas` (`desde`, `hasta`) · Always Output Data | |
| 4 | `Pedir abonos del día` | HTTP Request GET `/api/abonos` (`desde`, `hasta`) · Always Output Data | |
| 5 | `Sumar por forma de pago` | Code | Totales por `efectivo`/`tarjeta`/`bizum` para ventas y abonos, total general, recuento; redondeo a 2 decimales **solo del total** (`Math.round(total * 100) / 100`), nunca de cada importe (ADR-0002, D6); maneja listas vacías |
| 6 | `Guardar cierre` | <<PENDIENTE: Google Sheets append/update>> | |
| 7 | `Enviar resumen a Marisa` | Gmail (Send) | Texto distinto si no hubo movimientos |

## 2. Llamadas a la API de la tienda

| Método y ruta | Parámetros | Campos usados |
|---|---|---|
| `GET /api/ventas` | `desde`, `hasta` (AAAA-MM-DD, incluidas); sin `pagina` | `importe`, `forma_pago` |
| `GET /api/abonos` | `desde`, `hasta` | `importe`, `forma_pago` |

## 3. Credenciales y variables (solo nombres)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| `API tienda` (ADR-0002, D5) | Header Auth | API |
| <<PENDIENTE>> | Google Sheets OAuth2 | Histórico |
| <<PENDIENTE>> | Correo / Telegram | Resumen |

## 4. Manejo de errores

Error Workflow; Retry On Fail en las llamadas a la API.

## 5. Datos de prueba

`fixtures.md`: día normal, día vacío, solo una forma de pago.

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Consultar la API | Acumular eventos del webhook | Los avisos pueden perderse |
