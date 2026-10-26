# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 005 · Avisos de error (Error Workflow) — Spec

- **Estado:** Borrador
- **HU:** HU-05 · Avisos de errores (flujo 8)
- **Flujo enunciado:** FL-08 · Error Workflow
- **Nivel:** 🟢 Esencial
- **Redacta:** <<PENDIENTE>> · **Aprueba:** <<PENDIENTE>>
- **Fecha:** 2026-10-23

## 1. Objetivo

Que Marisa se entere en el momento si una automatización falla.

## 2. Historia de usuario

> Como **Marisa**, quiero que me avisen si una automatización falla, para no descubrir semanas después que algo dejó de funcionar.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Error Trigger | Se ejecuta cuando falla cualquier flujo que lo tenga asignado en *Settings → Error Workflow* |

## 4. Entradas

Datos que entrega el Error Trigger de n8n: nombre e id del flujo, id y URL de la ejecución, último nodo ejecutado, mensaje del error.

## 5. Salidas

| Salida | Destinatario | Contenido |
|---|---|---|
| Aviso de error | Marisa / tienda, Gmail (ADR-0002, D12) | Flujo, paso (nodo), mensaje del error, fecha y hora, enlace a la ejecución |

## 6. Reglas de negocio aplicables

Constitución III y VIII.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| El mensaje de error contiene una clave, token o cabecera | Se enmascara antes de enviarlo (`X-API-Key`, `Authorization`, `Bearer …`, `password`, `apiKey`) |
| Falla el propio envío del aviso | n8n no encadena Error Workflows; queda en *Executions*. <<PENDIENTE: ¿respaldo si falla el propio envío por Gmail?>> |
| Muchos errores seguidos | <<PENDIENTE: ¿agrupar avisos?>> (fuera del nivel esencial) |

## 8. Criterios de aceptación

- [ ] CA-1 Cualquier flujo que falle envía un aviso con el nombre del flujo, el paso y el error.
- [ ] CA-2 El aviso no incluye contraseñas ni claves.
- [ ] CA-3 Todos los flujos del repositorio tienen este Error Workflow asignado (lo comprueba `flow-reviewer`).

## 9. Datos personales

El mensaje de error puede contener datos de un cliente (p. ej. un email en el error de envío). <<PENDIENTE: decidir si se enmascaran también>>.

## 10. Fuera de alcance

Reintentar automáticamente el flujo fallido.

## 11. Preguntas abiertas

- ~~Canal~~ → resuelto: **Gmail** (ADR-0002, D12).
