# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 005 · Avisos de error — Plan

- **Estado del plan:** Borrador (no se construye hasta que la spec esté `Aprobada`)
- **Flujo n8n:** `[ERR] Avisos de error` → `automation/005-error-workflow.json` <<PENDIENTE: confirmar carpeta>>

## 1. Diseño del flujo

| # | Nodo | Tipo n8n | Qué hace |
|---|---|---|---|
| 1 | `Cuando falla un flujo` | Error Trigger | |
| 2 | `Preparar aviso sin secretos` | Code | Toma `workflow.name`, `execution.lastNodeExecuted`, `execution.error.message`, `execution.url`; enmascara patrones de secreto |
| 3 | `Avisar a la tienda` | <<PENDIENTE: canal>> | Retry On Fail |

## 2. Llamadas a la API de la tienda

Ninguna.

## 3. Credenciales y variables (solo nombres)

| Nombre en n8n | Tipo | Para qué |
|---|---|---|
| <<PENDIENTE>> | Correo / Telegram | Aviso |

## 4. Manejo de errores

Este flujo **no** se asigna a sí mismo como Error Workflow.

## 5. Datos de prueba

`fixtures.md`: un flujo de prueba que falla a propósito (nodo Stop and Error) con un mensaje que contiene una clave falsa.

## 6. Riesgos y decisiones

| Decisión | Alternativas | Por qué |
|---|---|---|
| Enmascarar en Code | Confiar en que los errores no traen secretos | Los errores HTTP pueden incluir cabeceras |
