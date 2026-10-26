# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 001 · Confirmación de apartado — Spec

- **Estado:** Borrador
- **HU:** HU-01 · Confirmación al apartar (flujo 1)
- **Flujo enunciado:** FL-01 · Confirmación de apartado
- **Nivel:** 🟢 Esencial
- **Redacta:** <<PENDIENTE>> · **Aprueba:** <<PENDIENTE>>
- **Fecha:** 2026-10-23

## 1. Objetivo

Que el cliente reciba al momento un resumen de lo que ha apartado, lo pagado, lo pendiente y la fecha límite.

## 2. Historia de usuario

> Como **cliente**, quiero recibir un mensaje al apartar unos zapatos, para tener claro qué he apartado, cuánto he pagado, cuánto me falta y hasta cuándo.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Evento `apartado.creado` | Llega desde el enrutador `000` (Execute Workflow Trigger) con `datos` = apartado |

## 4. Entradas

| Campo | Origen | Obligatorio | Notas |
|---|---|---|---|
| `id` | evento | Sí | Nº de apartado |
| `cliente` | evento | Sí | Para el saludo |
| `email` | evento | No | Si falta, ver §7 |
| `telefono` | evento | No | Solo si el canal es Telegram/SMS <<PENDIENTE>> |
| `producto`, `talla` | evento | `talla` puede ser `null` | |
| `precio`, `abonado`, `pendiente` | evento | Sí | **Se usan tal cual** (Constitución I) |
| `fecha_limite` | evento | Sí | `AAAA-MM-DD`; se muestra como `DD/MM/AAAA` |
| `estado` | evento | Sí | Puede ser `liquidado` si el abono inicial = precio |

## 5. Salidas

| Salida | Destinatario | Canal | Contenido |
|---|---|---|---|
| Confirmación | Cliente | <<PENDIENTE: correo (Gmail/SMTP) o Telegram>> | Nº apartado, producto, talla, precio, abonado, pendiente, fecha límite |
| Aviso de no envío | Tienda (Marisa) | Gmail (ADR-0002, D12) | «No se pudo enviar la confirmación del apartado #id: el cliente no tiene correo» |

## 6. Reglas de negocio aplicables

R-01, R-04 (informativas: ya las aplicó la app). Constitución I y IX.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| Sin `email` (y canal = correo) | No falla: avisa a la tienda con el nº de apartado y el nombre |
| `talla` nula | El mensaje omite la talla, sin mostrar «null» |
| `estado = liquidado` desde el alta | El mensaje indica que está pagado y puede recogerlos <<PENDIENTE: confirmar texto>> |
| Fallo del proveedor de correo | Error Workflow `005` |

## 8. Criterios de aceptación

- [ ] CA-1 Al crear un apartado en la app, el cliente recibe un mensaje en menos de un minuto.
- [ ] CA-2 El mensaje incluye modelo, talla, precio, abonado, pendiente y fecha límite, con los importes que da la app.
- [ ] CA-3 Si el cliente no tiene correo, el flujo no falla: avisa a la tienda de que no se pudo enviar.
- [ ] CA-4 Los importes se muestran con formato español (`79,90 €`) sin alterar su valor.

## 9. Datos personales

Nombre, email (y teléfono si el canal lo usa). Salen solo hacia el proveedor de mensajería. No se envían a modelos de IA.

## 10. Fuera de alcance

Redacción del mensaje con IA (nivel avanzado).

## 11. Preguntas abiertas

- ~~Canal de mensajes~~ → resuelto: **Gmail** para cliente y tienda (`docs/prd-nivel-medio.md` §1; ADR-0002, D12).
- <<PENDIENTE: remitente y asunto del correo>>
