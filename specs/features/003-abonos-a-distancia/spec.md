# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 003 · Abonos a distancia (Bizum / transferencia) — Spec

- **Estado:** Borrador
- **HU:** HU-03 · Abonos por Bizum o transferencia sin apuntar nada a mano (flujo 3)
- **Flujo enunciado:** FL-03 · Abonos a distancia
- **Nivel:** 🟢 Esencial
- **Redacta:** <<PENDIENTE>> · **Aprueba:** <<PENDIENTE>>
- **Fecha:** 2026-10-23

## 1. Objetivo

Registrar solos los pagos que llegan por Bizum o transferencia en el apartado correcto y, cuando no esté claro, **no registrar nada** y preguntar a Marisa.

## 2. Historia de usuario

> Como **Marisa**, quiero que los pagos que me llegan por Bizum o transferencia se registren solos en el apartado correcto, para dejar de revisar los avisos del banco y apuntarlos a mano.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Correo nuevo | Gmail Trigger sobre el buzón de la tienda (canal único Gmail, ADR-0002 D12) |
| Formulario (solo desarrollo) | Form Trigger con asunto y cuerpo, para probar sin correo |

## 4. Entradas

| Campo | Origen | Notas |
|---|---|---|
| Asunto, cuerpo, remitente | Correo | Remitente esperado del banco: <<PENDIENTE: confirmar dirección real>> |
| `ordenante`, `importe`, `concepto`, `tipo` (`bizum`/`transferencia`), `es_pago` | **Extraídos por IA** | Salida JSON con esquema fijo; el flujo valida tipos |
| Apartados activos | `GET /api/apartados?estado=activo` | Para casar nombre y nº de apartado |

## 5. Salidas

| Resultado | Acción |
|---|---|
| No es un pago | Se ignora (sin aviso) |
| Un único apartado claro, importe ≤ pendiente, dentro de plazo | `POST /api/apartados/{id}/abonos`. El recibo lo envía el flujo `002` gracias al evento `abono.registrado` |
| Dudoso: varios candidatos, sin concepto con solo apellido/inicial, o cliente desconocido | **No registra.** Pregunta a Marisa con los datos del aviso y los candidatos |
| Importe > pendiente | **No registra.** Avisa a Marisa con el motivo (422 de la app o comprobación previa) |
| Apartado fuera de plazo | **No registra.** Avisa a Marisa con el motivo |

## 6. Reglas de negocio aplicables

R-05, R-06, R-07, R-08. Constitución **II** (la IA solo extrae), I, IX.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| El concepto trae nº de apartado («apartado 2») | Manda el nº, aunque el ordenante esté abreviado; se comprueba que el nombre no contradice |
| Nombre con más apellidos o sin tildes («CARMEN RUIZ GARCIA», «LUCIA GOMEZ») | Comparación sin tildes ni mayúsculas, por palabras; `q=` de la API no ignora tildes |
| Transferencia | `transferencia` **no es una forma de pago de la app**: se registra con `forma_pago: "bizum"` y el aviso a Marisa indica que el origen era una transferencia (`docs/prd-nivel-medio.md` §6.4; ADR-0002, D12). Supuesto a confirmar con Marisa |
| La IA devuelve importe no numérico o JSON inválido | Se trata como dudoso y se pregunta a Marisa |
| El mismo correo se procesa dos veces | No debe duplicar el abono. <<PENDIENTE: marcar correo como leído/etiqueta o registro de ids procesados>> |
| La API responde 422 | Rama de error → aviso a Marisa con `detail` |

## 8. Criterios de aceptación

- [ ] CA-1 Los correos que no son un pago (como la publicidad del banco) se ignoran.
- [ ] CA-2 De cada pago se extraen ordenante, importe y concepto, y se busca el apartado por API.
- [ ] CA-3 Si hay un único apartado claro, se registra el abono y el cliente recibe su recibo (HU-02).
- [ ] CA-4 Si el pago es dudoso (varios apartados posibles, sin concepto o cliente desconocido), no se registra nada y se pregunta a Marisa.
- [ ] CA-5 Si el importe supera lo pendiente o el apartado está fuera de plazo, no se registra nada y se avisa a Marisa con el motivo.
- [ ] CA-6 El flujo resuelve bien los 9 correos de `data/correos/` (tabla en `fixtures.md`).
- [ ] CA-7 La IA nunca decide: el registro depende solo de nodos IF/Switch/Code y de la API.

## 9. Datos personales

Al modelo de IA solo se envía **asunto y cuerpo del aviso** (nombre del ordenante, importe, concepto). Nunca la lista de apartados, teléfonos ni emails. Modelo: <<PENDIENTE: modelo gratuito elegido y dónde se ejecuta>>.

## 10. Fuera de alcance

Responder al cliente por el mismo canal del banco; devolver pagos.

## 11. Preguntas abiertas

- ~~Forma de pago para transferencias~~ → resuelto: `bizum`, avisando a Marisa del origen (ADR-0002, D12).
- ~~Canal para preguntar a Marisa~~ → resuelto: **Gmail**. <<PENDIENTE: cómo responde ella (¿registra a mano en la app?)>>
- <<PENDIENTE: estrategia anti-duplicados>>
