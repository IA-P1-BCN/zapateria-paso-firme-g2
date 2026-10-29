# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 008 · Informe mensual — Plan

- **Spec:** `spec.md` (`Aprobada`)
- **Flujo n8n:** `[008] Informe mensual` → `workflows/008-informe-mensual.json`
- **Fecha:** 2026-10-29

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Calcular mes anterior` | Code (`n8n-nodes-base.code`) | Calcula `desde`, `hasta` (primer y último día del mes anterior) y `mes` (YYYY-MM) en `Europe/Madrid` (`ZONA_HORARIA`). Un único item |
| 2 | `Pedir ventas del mes` | HTTP Request (`n8n-nodes-base.httpRequest`) | `GET http://tienda:8000/api/ventas?desde=...&hasta=...` con credencial `PF · API tienda`, `alwaysOutputData: true` |
| 3 | `Pedir abonos del mes` | HTTP Request | `GET http://tienda:8000/api/abonos?desde=...&hasta=...` con credencial `PF · API tienda`, `alwaysOutputData: true` |
| 4 | `Pedir apartados activos` | HTTP Request | `GET http://tienda:8000/api/apartados?estado=activo` (sin `pagina`) con credencial `PF · API tienda`, `alwaysOutputData: true` |
| 5 | `Pedir todos los apartados` | HTTP Request | `GET http://tienda:8000/api/apartados` (sin `pagina`) con credencial `PF · API tienda`, `alwaysOutputData: true` |
| 6 | `Pedir vales` | HTTP Request | `GET http://tienda:8000/api/vales` con credencial `PF · API tienda`, `alwaysOutputData: true` |
| 7 | `Filtrar liquidados` | Code | De `Pedir todos los apartados`, emite solo los items con `estado = liquidado` (un item por apartado) |
| 8 | `Pedir detalle de liquidados` | HTTP Request | `GET http://tienda:8000/api/apartados/{{ $json.id }}` por cada item (modo por item), con credencial `PF · API tienda`, `alwaysOutputData: true` |
| 9 | `Sumar informe` | Code (`runOnceForAllItems`) | Agrega ventas, abonos, pendiente de activos, nuevos (por `fecha`), vencidos (vales por `fecha`), liquidados (por último abono en el mes). Redondea solo totales a 2 decimales. Prepara `asunto_correo` y `cuerpo_correo` (tabla HTML) |
| 10 | `Enviar informe a Marisa` | Gmail (`n8n-nodes-base.gmail`) | Envía el correo con la tabla HTML (o ceros + nota si no hay datos) a `MARISA_EMAIL` |

## 2. Llamadas a la API de la tienda

| Método y ruta | Cuándo | Parámetros | Campos de respuesta que se usan |
|---|---|---|---|
| `GET /api/ventas` | Tras calcular el mes anterior | `desde`, `hasta` (`AAAA-MM-DD`, incluidas) | `importe`, `forma_pago`, `fecha`, `concepto` |
| `GET /api/abonos` | Tras consultar las ventas del mes | `desde`, `hasta` (`AAAA-MM-DD`, incluidas) | `importe`, `forma_pago`, `fecha`, `apartado_id` |
| `GET /api/apartados` | Tras consultar los abonos del mes | `estado=activo` (sin `pagina`) | `pendiente` |
| `GET /api/apartados` | Tras consultar los activos | sin parámetros (sin `pagina`) | `id`, `fecha`, `estado` |
| `GET /api/vales` | Tras consultar los apartados | sin parámetros | `fecha`, `apartado_id`, `importe` |
| `GET /api/apartados/{id}` | Por cada apartado `liquidado` | `id` en la URL | `abonos[]` (con `fecha`) para aproximar la fecha de liquidación |

Comprobado con `api-contract-checker`: Sí (2026-10-29).

## 3. Credenciales y variables (solo nombres, nunca valores)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| `API tienda` | Header Auth (`X-API-Key`) | Autenticación contra `http://tienda:8000/api/...` |
| `Gmail tienda` | Gmail OAuth2 | Envío del informe a Marisa |
| `MARISA_EMAIL` | Variable n8n | Destinatario del informe |
| `ZONA_HORARIA` | Variable n8n | `Europe/Madrid` (cálculo del mes anterior y hora de disparo) |

Sin Google Sheets: este flujo no usa credencial de Sheets.

## 4. Manejo de errores

- Error Workflow asignado en `settings.errorWorkflow`: `[ERR] Avisos de error`.
- `alwaysOutputData: true` en todos los nodos HTTP Request para que una respuesta `[]` no detenga la ejecución.
- `retryOnFail: true` (`maxTries: 2`, `waitBetweenTries: 3000`) en los nodos HTTP Request y en el nodo Gmail.
- Las consultas de listas (`Pedir ventas del mes`, `Pedir abonos del mes`, `Pedir apartados activos`, `Pedir todos los apartados`, `Pedir vales`) no usan `On Error → Continue`: un 4xx/5xx propaga al Error Workflow `[ERR] Avisos de error`.
- Solo `Pedir detalle de liquidados` (N+1) usa `On Error → Continue (using error output)` para tratar 404/422 por apartado, avisar a Marisa con `detail` y continuar con el resto.
- Si un `GET /api/apartados/{id}` de un liquidado falla, se avisa a Marisa con el motivo y se continúa con el resto; el conteo de liquidados puede quedar incompleto (aproximación documentada).
- Si falla el envío del correo, reintento y, si persiste, Error Workflow.

## 5. Datos de prueba

Ver `fixtures.md` (casos: mes con datos, mes sin datos, liquidado por último abono, vencido, pendiente, reejecución).

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Consultar la API (`GET /api/ventas`, `GET /api/abonos`, `GET /api/apartados`, `GET /api/vales`) | Acumular eventos del webhook | Los avisos del webhook no tienen reintentos y pueden perderse; el informe debe ser autocontenido |
| Aproximar liquidados por último abono (`GET /api/apartados/{id}`) | Contar por `fecha` de creación | La app no guarda fecha de liquidación (dependencia PRD §5.3); usar el último abono es la aproximación aceptada |
| Tabla HTML en el correo | PDF o texto plano | Nivel Medio pide «informe en PDF o con tabla en el correo»; la tabla HTML es la opción más simple sin dependencias externas |
| Sin histórico en Google Sheets | Guardar en hoja `Informes` | El PRD no lo pide; evitar inventar almacenamiento auxiliar no definido |
| Sin desglose por forma de pago | Desglose efectivo/tarjeta/bizum | RF-37 solo exige separar ventas directas y abonos; el desglose queda como mejora futura |
| N+1 llamadas para liquidados | Un único endpoint agregado | La app no ofrece endpoint de agregación por mes; N+1 es aceptable (una vez al mes) |
| Sin idempotencia estricta | Guardar marca de envío | FL-07 no está en la lista de flujos idempotentes del PRD (RNF-05); reejecutar envía otro email |