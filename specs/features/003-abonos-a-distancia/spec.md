# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 003 · Abonos a distancia (Bizum / transferencia) — Spec

- **Estado:** Aprobada
- **HU:** HU-03 · Abonos por Bizum o transferencia sin apuntar nada a mano (flujo 3)
- **Flujo enunciado:** FL-03 · Abonos a distancia
- **Nivel:** 🟢 Esencial
- **Redacta:** <<PENDIENTE>> · **Aprueba:** <<PENDIENTE>>
- **Fecha:** 2026-10-23 · **Aprobada:** 2026-10-27

## 1. Objetivo

Registrar solos los pagos que llegan por Bizum o transferencia en el apartado correcto y, cuando no esté claro, **no registrar nada** y preguntar a Marisa.

## 2. Historia de usuario

> Como **Marisa**, quiero que los pagos que me llegan por Bizum o transferencia se registren solos en el apartado correcto, para dejar de revisar los avisos del banco y apuntarlos a mano.

## 3. Disparador

| Tipo | Detalle |
|---|---|
| Correo nuevo | Gmail Trigger sobre el buzón de la tienda (canal único Gmail, ADR-0002 D12), filtrado por la etiqueta de Gmail `Banco` |
| Pruebas (solo desarrollo) | Flujo `[TEST]` aparte con Form Trigger (asunto, cuerpo, remitente, `message_id` simulado). **No forma parte de `[003]`**, no se exporta ni se activa: un Form Trigger activo publica un formulario público |

## 4. Entradas

| Campo | Origen | Notas |
|---|---|---|
| `message_id`, remitente, asunto, cuerpo | Correo | `message_id` = id del mensaje en Gmail (los `.eml` de prueba no traen cabecera `Message-ID`; en pruebas se simula). Remitentes válidos en la variable `BANCO_REMITENTES`; no se fijan en el nodo |
| `es_pago`, `tipo` (`bizum`/`transferencia`/`desconocido`), `ordenante`, `importe`, `concepto`, `referencia_apartado` | **Extraídos por IA** | Salida JSON con esquema fijo; el flujo valida tipos. `referencia_apartado` solo si aparece explícita en el texto («apartado 2», «#2»); si no, `null` (`docs/prd-nivel-medio.md` §9.4, RF-15) |
| Apartados activos | `GET /api/apartados?estado=activo` | Para casar nombre y nº de apartado. Campos: `id`, `cliente`, `producto`, `pendiente`, `fecha_limite`, `estado` |
| Correos ya procesados | Data Table interna de n8n `Emails` (§7) | Clave `message_id` |

## 5. Salidas

| Resultado | Acción |
|---|---|
| Remitente fuera de `BANCO_REMITENTES` | Se ignora (sin aviso y sin llamar a la IA) |
| No es un pago (`es_pago: false`) | Se ignora (sin aviso) |
| Un único apartado claro, importe ≤ pendiente, dentro de plazo, **Bizum** | `POST /api/apartados/{id}/abonos` con `{importe, forma_pago: "bizum"}` (sin `fecha`: la app pone hoy). El recibo lo envía el flujo `002` gracias al evento `abono.registrado`. Sin aviso a Marisa |
| Igual, pero **transferencia** | Se registra con `forma_pago: "bizum"` y **se avisa a Marisa** de que el origen era una transferencia |
| Dudoso: varios candidatos, nombre abreviado sin concepto, cliente desconocido, referencia que contradice el nombre o extracción inválida | **No registra.** Pregunta a Marisa con los datos del aviso, los candidatos y el motivo |
| Importe > pendiente | **No registra.** Avisa a Marisa con el motivo (comprobación previa o `detail` del 422) |
| Apartado fuera de plazo o no `activo` | **No registra.** Avisa a Marisa con el motivo (comprobación previa o `detail` del 422) |

Marisa resuelve las dudas **registrando el abono a mano en la app** (pantalla de apartados); el flujo no lee respuestas a sus correos.

## 6. Reglas de negocio aplicables

R-05, R-06, R-07, R-08. Constitución **II** (la IA solo extrae), I, VIII, IX.

## 7. Casos de error y bordes

| Caso | Comportamiento esperado |
|---|---|
| El concepto trae nº de apartado («apartado 2») | Manda el nº, aunque el ordenante esté abreviado; se comprueba que el nombre no contradice. Si el nº no aparece literalmente en el correo (posible invención de la IA) → dudoso |
| La referencia apunta a un apartado que no está activo o cuyo cliente contradice al ordenante | Dudoso → pregunta a Marisa |
| Nombre con más apellidos o sin tildes («CARMEN RUIZ GARCIA», «LUCIA GOMEZ») | Comparación sin tildes ni mayúsculas, por palabras; `q=` de la API no ignora tildes |
| Transferencia | `transferencia` **no es una forma de pago de la app**: se registra con `forma_pago: "bizum"` y el aviso a Marisa indica que el origen era una transferencia (`docs/prd-nivel-medio.md` §6.4; ADR-0002, D12). Supuesto a confirmar con Marisa |
| La IA devuelve importe no numérico, JSON inválido o falla tras los reintentos | Se trata como dudoso y se pregunta a Marisa |
| Es un pago pero `tipo: "desconocido"` (no se sabe si es Bizum o transferencia) | Dudoso: no se registra y se pregunta a Marisa |
| El mismo correo se procesa dos veces | No duplica el abono. Se consulta el `message_id` en la Data Table `Emails` (PRD §8.6, en n8n en lugar de Google Sheets); si existe, termina. Se anota **antes** de registrar (estado `en_proceso`) y se actualiza al final con el resultado. Si el flujo falla a mitad, el correo queda `en_proceso`, no se reintenta solo y el Error Workflow avisa: es preferible un pago sin registrar (Marisa lo ve) a un abono duplicado |
| La API responde 422 o 404 | Rama de error → aviso a Marisa con `detail` |
| La API responde 401 | Error de configuración: Error Workflow `[ERR] Avisos de error`, sin reintentos |
| «Hoy» para el plazo | Se calcula en `Europe/Madrid` (variable `ZONA_HORARIA`), igual que la app |

## 8. Criterios de aceptación

- [ ] CA-1 Los correos que no son un pago (como la publicidad del banco) se ignoran.
- [ ] CA-2 De cada pago se extraen ordenante, importe, concepto y referencia, y se busca el apartado por API.
- [ ] CA-3 Si hay un único apartado claro, se registra el abono y el cliente recibe su recibo (HU-02). *Depende de `000` y `002`; hasta que existan se verifica solo el registro y la emisión del evento.*
- [ ] CA-4 Si el pago es dudoso (varios apartados posibles, sin concepto o cliente desconocido), no se registra nada y se pregunta a Marisa.
- [ ] CA-5 Si el importe supera lo pendiente o el apartado está fuera de plazo, no se registra nada y se avisa a Marisa con el motivo.
- [ ] CA-6 El flujo resuelve bien los 9 correos de `data/correos/` (tabla en `fixtures.md`). *El briefing dice «8 correos» en los criterios de entrega, pero su tabla, el PRD y la carpeta tienen 9.*
- [ ] CA-7 La IA nunca decide: el registro depende solo de nodos IF/Switch/Code y de la API.
- [ ] CA-8 Procesar dos veces el mismo correo no crea dos abonos (`docs/prd-nivel-medio.md` §9.4, RF-20).

## 9. Datos personales

Al modelo de IA solo se envía **asunto y cuerpo del aviso** (nombre del ordenante, importe, concepto). Nunca la lista de apartados, teléfonos ni emails de clientes. Modelo: **Google Gemini, capa gratuita** (servicio externo de Google; credencial `IA extracción`). Riesgo RGPD: en la capa gratuita Google puede usar el contenido enviado para mejorar sus productos; por eso solo se envía el aviso del banco y nunca datos de la app. <<PENDIENTE: modelo concreto de Gemini, a fijar al crear la credencial (T-003-06)>>. El almacén anti-duplicados guarda solo `message_id`, fecha, estado y `apartado_id` (sin nombres ni importes).

## 10. Fuera de alcance

Responder al cliente por el mismo canal del banco; devolver pagos; leer las respuestas de Marisa; verificar la autenticidad del banco más allá del remitente (SPF/DKIM los aplica Gmail).

## 11. Preguntas abiertas

- ~~Forma de pago para transferencias~~ → resuelto: `bizum`, avisando a Marisa del origen (ADR-0002, D12).
- ~~Canal para preguntar a Marisa~~ → resuelto: **Gmail**. Ella registra a mano en la app.
- ~~Estrategia anti-duplicados~~ → resuelto: Data Table `Emails` por `message_id`, anotando `en_proceso` antes de registrar (§7).
- ~~`referencia_apartado`~~ → resuelto: entra en el esquema de IA y el Code comprueba que aparece literalmente en el correo.
- ~~Remitente del banco~~ → resuelto: etiqueta de Gmail `Banco` + comprobación contra `BANCO_REMITENTES` (incluye la dirección de publicidad, para que la IA la descarte).
- ~~Form Trigger~~ → resuelto: solo en un flujo `[TEST]` local que no se exporta.
- ~~Modelo de IA~~ → resuelto: Gemini (capa gratuita), credencial `IA extracción` (§9).
- ~~Pago con `tipo: "desconocido"`~~ → resuelto: dudoso, se pregunta a Marisa (§7).
