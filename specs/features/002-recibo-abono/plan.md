# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 002 · Recibo de abono — Plan

- **Estado del plan:** Listo (spec `Aprobada` el 2026-10-26)
- **Flujo n8n:** `[002] Recibo de abono` → `workflows/002-recibo-abono.json`

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Recibir abono registrado` | Execute Workflow Trigger | Entrada desde `[000]` con `datos` en la raíz |
| 2 | `Configuración` | Set | `tienda_email` = `tienda@pasofirme.example`. Sustituye a `$vars` por si la instancia no tiene Variables |
| 3 | `Formatear importes y fechas` | Set | Formato español (`20,00 €`, `18/01/2027`), sin cambiar valores. La fecha se parte como texto, sin zona horaria. Talla nula → se omite |
| 4 | `¿Tiene correo?` | IF | `email` no nulo y no vacío tras quitar espacios |
| 5 | `¿Liquidado?` | IF (`estado` = `liquidado`) | Rama falsa → recibo |
| 6a | `Enviar recibo al cliente` | Gmail (Send) | Texto de la spec §5 |
| 6b | `Enviar aviso de recogida` | Gmail (Send) | Texto de la spec §5 |
| 6c | `Avisar a la tienda: sin correo` | Gmail (Send) | A `tienda_email`; añade la línea de liquidado si `estado = liquidado` |

No se llama a la API: el recibo no muestra la forma de pago (decisión de la spec §4).

## 2. Llamadas a la API de la tienda

Ninguna.

## 3. Credenciales y variables (solo nombres)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| `Correo tienda` | Gmail OAuth2 | Envíos al cliente y a la tienda (remitente «Zapatería Paso Firme») |
| `tienda_email` (nodo `Configuración`) | Valor en Set | Destinatario del aviso de no envío: `tienda@pasofirme.example` |

## 4. Manejo de errores

Error Workflow `[ERR] Avisos de error` (`settings.errorWorkflow`); Retry On Fail (2 intentos) en los tres envíos.

## 5. Datos de prueba

`fixtures.md`.

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Decidir por `estado` | Comprobar `pendiente == 0` | La app ya fija el estado; evita errores de redondeo |
| No llamar a la API | `GET /api/apartados/{id}` para `forma_pago` | La HU no lo pide; evita tratar 401/404 y otra credencial |
| Nodo Set `Configuración` | `$vars.TIENDA_EMAIL` | Funciona aunque la instancia no tenga Variables |
| Depende de `[000]` | — | Si `[000]` pasa los datos con otra forma, prevalece `[000]` y se ajusta el trigger |
