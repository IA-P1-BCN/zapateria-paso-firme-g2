# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 001 · Confirmación de apartado — Spec

- **Estado:** Aprobada
- **HU:** HU-01 · Confirmación al apartar (flujo 1)
- **Flujo enunciado:** FL-01 · Confirmación de apartado
- **Nivel:** 🟢 Esencial
- **Redacta:** Brian Hañari · **Aprueba:** Equipo Paso Firme (confirmada para construcción)
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
| `telefono` | evento | No | **No se usa**: el canal es Gmail (ADR-0002, D12) |
| `producto`, `talla` | evento | `talla` puede ser `null` | |
| `precio`, `abonado`, `pendiente` | evento | Sí | **Se usan tal cual** (Constitución I) |
| `fecha_limite` | evento | Sí | `AAAA-MM-DD`; se muestra como `DD/MM/AAAA` |
| `estado` | evento | Sí | Puede ser `liquidado` si el abono inicial = precio |

## 5. Salidas

| Salida | Destinatario | Canal | Contenido |
|---|---|---|---|
| Confirmación | Cliente | Gmail (nodo Gmail, credencial `Gmail tienda`) | Nº apartado, producto, talla, precio, abonado, pendiente, fecha límite |
| Aviso de no envío | Tienda (Marisa) | Gmail, misma credencial `Gmail tienda` | «No se pudo enviar la confirmación del apartado #id: el cliente no tiene correo» |

## 6. Reglas de negocio aplicables

R-01, R-04 (informativas: ya las aplicó la app). Constitución I y IX.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| Sin `email` (`null` o cadena vacía) | No falla: avisa a la tienda con el nº de apartado y el nombre |
| `talla` nula | El mensaje omite la talla, sin mostrar «null» |
| `estado = liquidado` desde el alta | El mensaje dice: «Ya está pagado: puedes recogerlo cuando quieras» y omite el pendiente |
| Fallo del proveedor de correo | Error Workflow `005` |

## 8. Criterios de aceptación

- [ ] CA-1 Al crear un apartado en la app, el cliente recibe un mensaje en menos de un minuto.
- [ ] CA-2 El mensaje incluye modelo, talla, precio, abonado, pendiente y fecha límite, con los importes que da la app.
- [ ] CA-3 Si el cliente no tiene correo, el flujo no falla: avisa a la tienda de que no se pudo enviar.
- [ ] CA-4 Los importes se muestran con formato español (`79,90 €`) sin alterar su valor.

## 9. Datos personales

Nombre y email del cliente. Salen únicamente hacia Gmail (Google) como proveedor de correo, con la credencial
`Gmail tienda`. El teléfono llega en el evento pero **no se usa** en este flujo. No se envían a modelos de IA.

## 10. Fuera de alcance

Redacción del mensaje con IA (nivel avanzado).

## 11. Preguntas abiertas

- ~~Canal de mensajes~~ → resuelto: **Gmail** para cliente y tienda (`docs/prd-nivel-medio.md` §1; ADR-0002, D12).
- **Remitente:** la cuenta de la credencial `Gmail tienda`.
  Aviso a la tienda: `correo_tienda` = `tienda@pasofirme.example` (el mismo que `tienda_email` de `002`); en n8n se pone el buzón real.
- **Asunto (propuesto):** `Confirmación de tu apartado · Paso Firme`. El número de apartado va en el cuerpo, no en el asunto.
