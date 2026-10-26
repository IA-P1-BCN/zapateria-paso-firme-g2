# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 002 · Recibo de abono — Spec

- **Estado:** Borrador
- **HU:** HU-02 · Recibo de cada abono (flujo 2)
- **Flujo enunciado:** FL-02 · Recibo de abono
- **Nivel:** 🟢 Esencial
- **Redacta:** <<PENDIENTE>> · **Aprueba:** <<PENDIENTE>>
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

El evento **no** trae `forma_pago` ni id del abono. Si el recibo debe mostrarlos: `GET /api/apartados/{id}` y tomar el último de `abonos` <<PENDIENTE: decidir si hace falta>>.

## 5. Salidas

| Salida | Cuándo | Destinatario | Contenido |
|---|---|---|---|
| Recibo | `estado = activo` | Cliente | Importe pagado, total abonado, pendiente, fecha límite |
| Aviso de recogida | `estado = liquidado` | Cliente | Importe pagado y que ya puede recoger sus zapatos |
| Aviso de no envío | Sin `email` | Tienda | Nº apartado y nombre |

## 6. Reglas de negocio aplicables

R-07, R-09 (ya aplicadas por la app). Constitución I.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| Sin `email` | No falla: avisa a la tienda |
| `pendiente = 0` y `estado = liquidado` | Mensaje de recogida, no de recibo |
| Fallo del envío | Reintento y Error Workflow `005` |

## 8. Criterios de aceptación

- [ ] CA-1 Cada abono registrado genera un recibo con el importe pagado y lo que queda pendiente.
- [ ] CA-2 Si el apartado queda liquidado, el mensaje cambia: avisa de que ya puede recoger sus zapatos.
- [ ] CA-3 La decisión recibo/recogida se toma con `datos.estado`, sin recalcular.
- [ ] CA-4 Sin correo, el flujo no falla y avisa a la tienda.

## 9. Datos personales

Nombre y email del cliente, solo hacia el proveedor de mensajería.

## 10. Fuera de alcance

Mostrar el historial completo de abonos.

## 11. Preguntas abiertas

- ~~Canal~~ → resuelto: **Gmail** (mismo que 001; ADR-0002, D12).
- <<PENDIENTE: ¿mostrar forma de pago en el recibo?>>
