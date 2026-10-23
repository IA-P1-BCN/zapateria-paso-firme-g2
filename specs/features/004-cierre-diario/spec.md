# SCOPE: infraestructura-agentes (NO tocar backend/frontend/automation)

# 004 · Cierre diario — Spec

- **Estado:** Borrador
- **HU:** HU-04 · Cierre de caja automático (flujo 5)
- **Nivel:** 🟢 Esencial
- **Redacta:** <<PENDIENTE>> · **Aprueba:** <<PENDIENTE>>
- **Fecha:** 2026-10-23

## 1. Objetivo

Cada noche, calcular lo cobrado en el día por forma de pago, guardar el cierre y enviárselo a Marisa.

## 2. Historia de usuario

> Como **Marisa**, quiero recibir cada noche el resumen de lo cobrado en el día, para cerrar la caja sin sumar con calculadora.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Schedule Trigger | Cada día a las <<PENDIENTE: hora, p. ej. 21:30>> (zona `Europe/Madrid`, ya configurada en `docker-compose.yml`) |

## 4. Entradas

| Campo | Origen | Notas |
|---|---|---|
| Ventas del día | `GET /api/ventas?desde=HOY&hasta=HOY` | `importe`, `forma_pago` |
| Abonos del día | `GET /api/abonos?desde=HOY&hasta=HOY` | Incluye abonos iniciales |

No depende de los avisos del webhook (pueden perderse).

## 5. Salidas

| Salida | Destino | Contenido |
|---|---|---|
| Registro del cierre | <<PENDIENTE: Google Sheets, hoja «Cierres»>> | Fecha, ventas/abonos/total por `efectivo`, `tarjeta`, `bizum`, total general, nº de movimientos |
| Resumen | Marisa, <<PENDIENTE: canal>> | Lo mismo, legible |

## 6. Reglas de negocio aplicables

Métrica «Ventas del día» (`ontology.md` §7). Sumar movimientos es trabajo de n8n (Constitución I lo permite).

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| Día sin movimientos | El resumen dice «Hoy no hubo movimientos» en vez de fallar (ojo: n8n no ejecuta los nodos siguientes si llegan 0 items → activar «Always Output Data») |
| Una forma de pago sin movimientos | Aparece con 0,00 € |
| La API no responde | Retry y Error Workflow `005` |
| Se ejecuta dos veces el mismo día | <<PENDIENTE: ¿sobrescribir la fila del día o añadir otra?>> |

## 8. Criterios de aceptación

- [ ] CA-1 Cada noche llega un resumen con ventas directas, abonos y el total, separados por forma de pago (efectivo, tarjeta y Bizum).
- [ ] CA-2 Los importes coinciden con los de la app.
- [ ] CA-3 Si ese día no hubo movimientos, el resumen lo dice en vez de fallar.
- [ ] CA-4 El cierre queda guardado fuera de la app (la app no guarda cierres).
- [ ] CA-5 Las sumas se redondean a 2 decimales.

## 9. Datos personales

Ninguno: ventas y abonos no llevan datos de cliente en estas consultas.

## 10. Fuera de alcance

Recaudación mensual (feature `008`).

## 11. Preguntas abiertas

- <<PENDIENTE: hora, destino del histórico, canal>>
