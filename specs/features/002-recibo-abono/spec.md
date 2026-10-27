# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 002 · Recibo de abono — Spec

- **Estado:** Aprobada
- **HU:** HU-02 · Recibo de cada abono (flujo 2)
- **Flujo enunciado:** FL-02 · Recibo de abono
- **Nivel:** 🟢 Esencial
- **Redacta:** levifvy (con Claude Code) · **Aprueba:** levifvy · **Fecha aprobación:** 2026-10-26
- **Fecha:** 2026-10-23

## 1. Objetivo

Enviar al cliente un recibo cada vez que abona, y avisarle de que puede recoger los zapatos cuando el apartado queda liquidado.

## 2. Historia de usuario

> Como **cliente**, quiero un recibo cada vez que pago un abono, para saber cuánto me queda por pagar.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Evento `abono.registrado` | Desde el enrutador `000`. Se dispara tanto si el abono lo registra la dependienta como si lo registra el flujo `003` |

## 4. Entradas

| Campo | Origen | Obligatorio | Notas |
|---|---|---|---|
| `id` | evento | Sí | **Id del apartado**, no del abono |
| `importe` | evento | Sí | Lo que se acaba de abonar |
| `abonado`, `pendiente`, `estado` | evento | Sí | Estado **después** del abono. Se usan tal cual |
| `cliente`, `email`, `producto`, `talla`, `precio`, `fecha_limite` | evento | `email`, `talla` opcionales | |

El evento **no** trae `forma_pago` ni id del abono. **Decisión:** el recibo no los muestra; el flujo no llama a la API.
`email` se considera ausente si es `null`, cadena vacía o solo espacios.

## 5. Salidas

| Salida | Cuándo | Destinatario | Contenido |
|---|---|---|---|
| Recibo | `estado ≠ liquidado` con email | Cliente | Nº apartado, producto, talla (si hay), importe pagado, total abonado, pendiente, fecha límite |
| Aviso de recogida | `estado = liquidado` con email | Cliente | Nº apartado, producto, talla (si hay), importe pagado, total abonado, que ya puede recogerlos |
| Aviso de no envío | Sin `email` | Tienda (`tienda_email`) | Nº apartado, nombre, importe pagado y si ha quedado liquidado |

Canal: Gmail, credencial `Correo tienda`, remitente «Zapatería Paso Firme».

**Textos** (importes `20,00 €`, fechas `DD/MM/AAAA`):

- Recibo · Asunto: `Recibo de tu abono · Apartado nº {id}`
  «Hola {cliente}: hemos recibido tu abono de {importe} para el apartado nº {id} ({producto}[, talla {talla}]).
  Total abonado: {abonado}. Pendiente: {pendiente}. Fecha límite para completar el pago: {fecha_limite}.
  Gracias por tu confianza. Zapatería Paso Firme»
- Recogida · Asunto: `¡Ya puedes recoger tus zapatos! · Apartado nº {id}`
  «Hola {cliente}: hemos recibido tu abono de {importe} y tu apartado nº {id} ({producto}[, talla {talla}])
  está pagado por completo ({abonado}). Ya puedes pasar por la tienda a recogerlos. Zapatería Paso Firme»
- Tienda · Asunto: `Recibo no enviado · Apartado nº {id}`
  «No se pudo enviar el recibo del abono de {importe} del apartado nº {id} ({cliente}): el cliente no tiene correo.
  [El apartado ha quedado liquidado: avisadle para que recoja los zapatos.]»

## 6. Reglas de negocio aplicables

R-07, R-09 (ya aplicadas por la app). Constitución I.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| Sin `email` | No falla: avisa a la tienda |
| `email` vacío o solo espacios | Igual que sin `email` |
| Sin `email` y `estado = liquidado` | Aviso a la tienda indicando que ha quedado liquidado |
| `pendiente = 0` y `estado = liquidado` | Mensaje de recogida, no de recibo |
| `talla` nula | Se omite «, talla …» (nunca «null») |
| Importes con decimales (`59.9`, `0.1`) | Se muestran `59,90 €`, `0,10 €` sin cambiar el valor |
| `fecha_limite` `2027-01-18` | Se muestra `18/01/2027`, sin desfase por zona horaria |
| Fallo del envío | Retry On Fail (2 intentos) y después Error Workflow `[ERR] Avisos de error` |

## 8. Criterios de aceptación

- [ ] CA-1 Cada abono registrado que deja el apartado `activo` genera un recibo con el importe pagado y lo que queda pendiente.
- [ ] CA-2 Si el apartado queda liquidado, el mensaje cambia: avisa de que ya puede recoger sus zapatos.
- [ ] CA-3 La decisión recibo/recogida se toma con `datos.estado`, sin recalcular.
- [ ] CA-4 Sin correo, el flujo no falla y avisa a la tienda.

## 9. Datos personales

Nombre y email del cliente, producto y talla, solo hacia Gmail. Sin IA. Mensaje transaccional: no necesita consentimiento (`docs/prd-completo.md` §5).

## 10. Fuera de alcance

Mostrar el historial completo de abonos.

## 11. Preguntas abiertas

- ~~Canal~~ → resuelto: **Gmail** (mismo que 001; ADR-0002, D12).
- ~~¿Forma de pago?~~ → no se muestra.
- ~~Valor de `tienda_email`~~ → `tienda@pasofirme.example` (nodo Set `Configuración`; confirmado por levifvy el 2026-10-26).
- Dependencias: `[000]` (Execute Workflow con `datos` en la raíz; pregunta abierta en `000/spec.md:72`) y `[ERR]` (spec 005).
