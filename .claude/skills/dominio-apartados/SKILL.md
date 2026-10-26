---
# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)
name: dominio-apartados
description: Reglas del negocio de la zapatería (apartados, abonos, liquidación, vencimiento, vales, formas de pago) y qué calcula la app frente a lo que calcula n8n. Úsala siempre que un flujo, spec o mensaje trate importes, estados de apartado, plazos o identificación de clientes.
---

# Dominio: sistema de apartados

Modelo completo en `ontology.md`. Esto es la chuleta para decidir rápido.

## Reglas (IDs de `ontology.md` §6)

| ID | Regla | Lo aplica |
|---|---|---|
| R-01/02 | Abono inicial ≥ 5 € y ≤ precio | App (422) |
| R-04 | `fecha_limite` = fecha + 90 días | App |
| R-05 | Solo se abona un `activo` | App (422) |
| R-06 | No se abona después de `fecha_limite` (el mismo día sí) | App (422) |
| R-07 | Abono > 0 y ≤ `pendiente` | App (422) |
| R-08 | `forma_pago` ∈ {efectivo, tarjeta, bizum} | App (422) |
| R-09 | `pendiente` = 0 → `liquidado` automático | App |
| R-10 | Vencer solo si `activo` y hoy > `fecha_limite` | App (422); **lo dispara n8n** |
| R-11 | Vencer genera vale `VALE-NNNNN` = `abonado` | App |

## Qué calcula quién

| Dato | Quién | n8n puede… |
|---|---|---|
| `abonado`, `pendiente`, `estado`, `fecha_limite` | App | Leer y formatear. **Nunca recalcular** |
| Código e importe del vale | App | Leer |
| Totales del día / mes por forma de pago | n8n | Sumar ventas y abonos de la API; redondear a 2 decimales solo el total, nunca cada importe (ADR-0002, D6) |
| Total pendiente de cobro | n8n | Sumar `pendiente` de `GET /api/apartados?estado=activo` |
| ¿Faltan 7 o 1 días? | n8n | Comparar `fecha_limite` con hoy (zona Europe/Madrid) |

## Trampas habituales

- Un apartado con el plazo pasado **sigue `activo`** hasta que n8n llama a `/vencer`.
- `abono.registrado` trae en `id` el **id del apartado**, y no trae `forma_pago`.
- No existe la forma de pago `transferencia` ni una entidad Cliente: identificar por nombre es ambiguo. Ante la duda, **preguntar a Marisa**; no adivinar.
- `GET /api/apartados?q=` usa `LIKE`: no ignora tildes ni apellidos extra.
- Los datos de ejemplo se generan con fechas relativas al día de arranque: para repetir pruebas, `docker compose down -v && docker compose up -d`.

## Validar en un nodo Code (patrón)

```js
// Solo validaciones previas para dar un motivo claro; la app sigue siendo quien decide (422).
const a = $json.apartado;        // de la API
const importe = Number($json.importe);
const hoy = $now.toFormat('yyyy-MM-dd');
let motivo = null;
if (a.estado !== 'activo') motivo = `El apartado está ${a.estado}`;
else if (hoy > a.fecha_limite) motivo = 'El plazo del apartado ha vencido';
else if (!(importe > 0)) motivo = 'Importe no válido';
else if (importe > a.pendiente) motivo = `El importe supera lo pendiente (${a.pendiente} €)`;
return [{ json: { ...$json, puede_abonar: motivo === null, motivo } }];
```
