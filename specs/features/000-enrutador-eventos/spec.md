# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 000 · Enrutador de eventos — Spec

- **Estado:** Borrador
- **HU:** requisito del nivel esencial («un único webhook que reparta los eventos con un nodo Switch según el campo `evento`»)
- **Nivel:** 🟢 Esencial
- **Redacta:** <<PENDIENTE>> · **Aprueba:** <<PENDIENTE>>
- **Fecha:** 2026-10-23

## 1. Objetivo

Tener **un solo punto de entrada** para todos los avisos de la app y repartir cada evento al flujo que le toca, para que el resto de flujos no dependan de la URL del webhook.

## 2. Historia de usuario

> Como **equipo**, queremos un único webhook con un Switch por `evento`, para que añadir o cambiar un flujo no obligue a tocar la configuración de la app.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Webhook n8n | `POST`, path `tienda` → Production URL `http://n8n:5678/webhook/tienda` (la que trae `.env.example`) |

## 4. Entradas

| Campo | Origen | Obligatorio | Notas |
|---|---|---|---|
| `body.evento` | Webhook | Sí | `apartado.creado` · `abono.registrado` · `venta.registrada` · `apartado.vencido` |
| `body.datos` | Webhook | Sí | Forma según el evento (ver skill `tienda-api`) |

## 5. Salidas

| Salida | Destino |
|---|---|
| `apartado.creado` | Flujo `001` (confirmación) |
| `abono.registrado` | Flujo `002` (recibo) |
| `venta.registrada` | Flujo `006` (venta grande) cuando exista; mientras, no hace nada |
| `apartado.vencido` | Flujo `007` (aviso de vale) cuando exista; mientras, no hace nada |
| Evento desconocido | No falla; queda registrado en la ejecución (rama *fallback*) |

## 6. Reglas de negocio aplicables

Ninguna regla de importes. Constitución I (se reenvía `datos` tal cual, sin transformar importes).

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| `evento` desconocido o vacío | Rama *fallback*; la ejecución termina bien y no avisa al cliente |
| Falla un flujo hijo | Lo recoge el Error Workflow (`005`); el enrutador no reintenta |
| n8n caído cuando la app avisa | El aviso se pierde (la app no reintenta). Fuera de alcance: los flujos programados cubren los datos críticos |

## 8. Criterios de aceptación

- [ ] CA-1 Con el flujo publicado, crear un apartado en la app produce una ejecución del enrutador que llega a la rama `apartado.creado`.
- [ ] CA-2 Cada uno de los 4 eventos sale por su rama (comprobado con los payloads de `fixtures.md`).
- [ ] CA-3 Un evento desconocido no produce error.
- [ ] CA-4 Las expresiones leen `{{ $json.body.evento }}`, no `{{ $json.evento }}`.

## 9. Datos personales

Recibe nombre, teléfono y email del cliente. No los envía a terceros; solo los pasa a los flujos hijos.

## 10. Fuera de alcance

- Autenticar el webhook (HU-14): la app no envía cabecera de autenticación y no se puede tocar el backend. Ver `specs/backlog.md`.

## 11. Preguntas abiertas

- <<PENDIENTE: ¿los flujos hijos se llaman con Execute Workflow (sub-flujos) o el enrutador contiene las ramas? Recomendado: Execute Workflow, un flujo por HU, para repartir el trabajo sin conflictos>>
