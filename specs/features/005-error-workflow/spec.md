# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 005 · Avisos de error (Error Workflow) — Spec

- **Estado:** Aprobada
- **HU:** HU-05 · Avisos de errores (flujo 8)
- **Flujo enunciado:** FL-08 · Error Workflow
- **Nivel:** 🟢 Esencial
- **Redacta:** BrianStiv (con OpenCode/GLM) · **Aprueba:** BrianStiv
- **Fecha:** 2026-10-23
- **Actualizada:** 2026-10-29 (enmascarado RGPD decidido, credencial fijada a `Gmail tienda`, agrupación fuera de alcance, respaldo propuesto — ver §10 y §11)

## 1. Objetivo

Que Marisa se entere en el momento si una automatización falla.

## 2. Historia de usuario

> Como **Marisa**, quiero que me avisen si una automatización falla, para no descubrir semanas después que algo dejó de funcionar.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Error Trigger | Se ejecuta cuando falla cualquier flujo que lo tenga asignado en *Settings → Error Workflow* |

La asignación se hace en n8n (abriendo cada flujo: *Settings → Error workflow*). En el JSON exportado cada flujo de `workflows/` la importa como tarea humana: `flow-reviewer` comprueba que ningún flujo quede sin ella (CA-3, Constitución VIII).

## 4. Entradas

Datos que entrega el Error Trigger de n8n en el item de entrada:

| Dato | Uso |
|---|---|
| Flujo fallido: nombre e id (`workflow`) | Encabezado del aviso |
| Ejecución: id y URL (`execution.url`) | Enlace del aviso, para ver el detalle completo en n8n |
| Último nodo ejecutado (`lastNodeExecuted`) | Paso donde se rompió |
| Mensaje del error y, si lo hay, stack (`execution.error`) | Descripción técnica del fallo |

El mensaje del error lo genera el nodo que falla: puede venir de la API (401/404/422 con `{"detail": "..."}`, ver `docs/guia-de-la-app.md`), de un nodo Gmail, de una expresión, etc.

`<<PENDIENTE: confirmar en n8n la estructura exacta del Error Trigger al importar y probar (varía entre versiones; se fijará en fixtures.md)>>`.

## 5. Salidas

| Salida | Destinatario | Contenido |
|---|---|---|
| Aviso de error | La tienda, Gmail (nodo Gmail, credencial `Gmail tienda`; ADR-0002, D12) | Flujo, paso (nodo), mensaje del error enmascarado, fecha y hora, enlace a la ejecución |

- **Credencial:** la misma `Gmail tienda` (Gmail OAuth2) que usa el flujo 001. **No se crea ninguna credencial nueva.**
- **Destinatario:** la cuenta de la tienda, coherente con la variable `correo_tienda` del nodo Configuración del flujo 001. `<<PENDIENTE: dirección real de la tienda (la crea Levi con el OAuth del equipo)>>`.

## 6. Reglas de negocio aplicables

Constitución III (cero secretos), VIII (los fallos se ven) y IX (mínimos datos personales). No hay reglas R-0x del dominio: este flujo no habla de apartados ni importes.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| El mensaje de error contiene una clave o token | Se enmascara antes de enviarlo (`X-API-Key`, `Authorization`, `Bearer …`, `password`, `apiKey`): se envía `***` en lugar del valor |
| El mensaje de error contiene datos personales de un cliente (email, teléfono, nombre) | Se **enmascara / no se incluye**: el aviso lleva siempre lo formal (flujo, nodo, enlace a la ejecución) y el mensaje técnico con los datos eliminados. Ver §9 |
| Falla el propio envío del aviso (Gmail caído, credencial expirada) | n8n **no encadena Error Workflows**, así que el fallo queda registrado como ejecución fallida en *Executions*. Sin decisión de la constitución que lo exija, el respaldo por otro canal queda como propuesta en §11 y fuera del nivel esencial |
| Muchos errores seguidos (p. ej. todas las ejecuciones de la mañana fallan) | Se envía un aviso por cada error, sin agrupar: la agrupación de avisos queda **fuera del nivel esencial** (ver §10); se puede añadir más adelante si la tienda lo pide |

## 8. Criterios de aceptación

Los dos primeros son los del enunciado (HU-05, literales, amplificados); los tres se mantienen.

- [ ] CA-1 Cualquier flujo que falle envía un aviso con el nombre del flujo, el paso y el error.
- [ ] CA-2 El aviso no incluye contraseñas, claves **ni datos personales de clientes**.
- [ ] CA-3 Todos los flujos del repositorio tienen este Error Workflow asignado (lo comprueba `flow-reviewer`).

## 9. Datos personales

**Regla aprobada (RGPD, mínimo imprescindible — Constitución IX):** el aviso **enmascara y, si cabe, no incluye** datos personales que aparezcan en el mensaje de error: emails de clientes, teléfonos, nombres de cliente. El aviso sirve para diagnosticar el flujo (qué falló y dónde), no para transportar datos de clientes; el detalle completo, con los datos, queda a un clic en el **enlace a la ejecución** de n8n.

Datos que sí salen del Error Workflow hacia Gmail: nombre del flujo fallido, último nodo ejecutado, mensaje técnico del error (con las máscaras de §7), fecha y hora, URL de la ejecución. No se envían datos a modelos de IA. Por ir al correo de la tienda con la misma credencial `Gmail tienda` que el resto de flujos, el proveedor sigue siendo Google.

## 10. Fuera de alcance

- Reintentar automáticamente el flujo fallido.
- Agrupar avisos cuando varios errores llegan seguidos (nivel esencial lo deja sin agrupar; se puede añadir más adelante).
- Respaldo por otro canal (Telegram, SMS…) si falla el propio envío del aviso: se propone en §11 como nivel medio, no esencial en esta spec.

## 11. Preguntas abiertas

- ~~Canal~~ → resuelto: **Gmail** (ADR-0002, D12). Credencial: la misma `Gmail tienda` del flujo 001; **no hay credencial nueva**.
- ~~Fechas~~ → resuelto.
- **Dirección de la tienda (destinatario del aviso):** coherente con la variable `correo_tienda` del flujo 001. `<<PENDIENTE: valor real, lo crea Levi con el OAuth del equipo>>`.
- **Respaldo si falla el propio envío del aviso (propuesta razonada, decisión humana):**
  n8n no encadena Error Workflows (un Error Workflow no puede asignarse a otro Error Workflow — concretamente, la ejecución fallida de este flujo no dispara otro aviso), así que el fallo queda visible solo en *Executions* de n8n. Propuesta: **no esencial** para el nivel actual; como mejora a nivel medio, en el nodo `Enviar aviso` marcar *On Error → Continue (using error output)* y mandar el fallo del envío a un **aviso secundario por otro canal** (p. ej. mensajería, que ya se propone para los niveles medio/avanzado del proyecto). Se marca `<<PENDIENTE: ¿activar en nivel medio? — decisión de Brian>>`.
- **Estructura exacta del Error Trigger** (§4): `<<PENDIENTE: confirmar al importar/probar y fijar en fixtures.md>>` (no es riesgo de la spec: se descubre con los datos de prueba).
