# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 004 · Cierre diario — Spec

- **Estado:** Aprobada
- **HU:** HU-04 · Cierre de caja automático (flujo 5)
- **Flujo enunciado:** FL-05 · Cierre diario
- **Nivel:** 🟢 Esencial
- **Redacta:** Miguel Matesanz · **Aprueba:** Levi Flores
- **Fecha:** 2026-10-28

## 1. Objetivo

Cada noche, calcular lo cobrado en el día por forma de pago, guardar el cierre y enviárselo a Marisa.

## 2. Historia de usuario

> Como **Marisa**, quiero recibir cada noche el resumen de lo cobrado en el día, para cerrar la caja sin sumar con calculadora.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Schedule Trigger | Cada día a las `21:30` (zona `Europe/Madrid`, ya configurada en `docker-compose.yml`) |

## 4. Entradas

| Campo | Origen | Notas |
|---|---|---|
| Ventas del día | `GET /api/ventas?desde=HOY&hasta=HOY` | `importe`, `forma_pago` |
| Abonos del día | `GET /api/abonos?desde=HOY&hasta=HOY` | Incluye abonos iniciales (`importe`, `forma_pago`) |

No depende de los avisos del webhook (pueden perderse).

## 5. Salidas

| Salida | Destino | Contenido |
|---|---|---|
| Registro del cierre | Google Sheets, hoja «Cierres» | `fecha`, ventas/abonos/total por `efectivo`, `tarjeta`, `bizum`, `total_general`, `num_movimientos` |
| Resumen | Marisa, Gmail (ADR-0002, D12) | Lo mismo, formateado y legible en español |

## 6. Reglas de negocio aplicables

Métrica «Ventas del día» (`ontology.md` §7). Sumar movimientos es trabajo de n8n (Constitución I lo permite). Nunca se redondean los sumandos individuales; solo cada total resultante se redondea a 2 decimales (ADR-0002, D6).

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| Día sin movimientos | El resumen dice «Hoy no hubo movimientos» en vez de fallar (activar «Always Output Data» en ambos nodos HTTP Request para que n8n continúe cuando llegan 0 items) |
| Una forma de pago sin movimientos | Aparece con `0,00 €` |
| La API no responde | Retry On Fail (2 intentos) y Error Workflow `[ERR] Avisos de error` (`005`) |
| Se ejecuta dos veces el mismo día | Sobrescribir la fila del día en Google Sheets mediante operación Upsert (`appendOrUpdate`) usando la columna `fecha` como clave |

## 8. Criterios de aceptación

- [ ] CA-1 Cada noche llega un resumen con ventas directas, abonos y el total, separados por forma de pago (efectivo, tarjeta y Bizum).
- [ ] CA-2 Los importes coinciden con los de la app.
- [ ] CA-3 Si ese día no hubo movimientos, el resumen lo dice en vez de fallar.
- [ ] CA-4 El cierre queda guardado fuera de la app (Google Sheets, hoja `Cierres`).
- [ ] CA-5 Los importes de la app no se redondean; solo cada **total** sumado se redondea a 2 decimales para quitar el error de coma flotante (ADR-0002, D6).

## 9. Datos personales

Ninguno: ventas y abonos no llevan datos de cliente en estas consultas (`VentaOut` y `AbonoOut` solo contienen identificadores, fechas, conceptos/importes y forma de pago).

## 10. Fuera de alcance

Recaudación mensual (feature `008`).

## 11. Preguntas abiertas

- Resueltas: hora `21:30` (`Europe/Madrid`), histórico en Google Sheets (hoja `Cierres` con upsert por `fecha`) y envío por Gmail a Marisa.
