# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# 008 · Informe mensual — Fixtures

Entradas = respuestas de la API (listas) del flujo `[008] Informe mensual`. Datos ficticios (nombres inventados, emails `@example.com`, teléfonos `6xx 000 xxx`). Mes de referencia en todos los casos salvo indicación: **ejecución el 2026-11-01 a las 08:00 `Europe/Madrid` → mes anterior = octubre 2026 (`desde=2026-10-01`, `hasta=2026-10-31`)**.

Se prueban con *Pin Data* en los nodos HTTP Request (`Pedir ventas del mes`, `Pedir abonos del mes`, `Pedir apartados activos`, `Pedir todos los apartados`, `Pedir vales`, `Pedir detalle de liquidados`), o con los datos de ejemplo de la app (`backend/seed.py`).

Los importes se muestran como `X,XX € (X.XX)`; los totales se redondean a 2 decimales; los sumandos no se alteran (RNF-14).

## F-008-1 Mes con datos (CA-1, CA-2, CA-3, CA-4)

**Ventas (`GET /api/ventas?desde=2026-10-01&hasta=2026-10-31`):**
```json
[
  {"id": 101, "fecha": "2026-10-05", "concepto": "Botín piel marrón T38", "importe": 89.9, "forma_pago": "efectivo"},
  {"id": 102, "fecha": "2026-10-12", "concepto": "Plantillas gel", "importe": 12.0, "forma_pago": "tarjeta"},
  {"id": 103, "fecha": "2026-10-20", "concepto": "Crema calzado", "importe": 4.5, "forma_pago": "bizum"}
]
```

**Abonos (`GET /api/abonos?desde=2026-10-01&hasta=2026-10-31`):**
```json
[
  {"id": 201, "apartado_id": 5, "fecha": "2026-10-08", "importe": 20.0, "forma_pago": "efectivo"},
  {"id": 202, "apartado_id": 7, "fecha": "2026-10-15", "importe": 10.0, "forma_pago": "tarjeta"},
  {"id": 203, "apartado_id": 5, "fecha": "2026-10-25", "importe": 15.0, "forma_pago": "bizum"}
]
```

**Apartados activos (`GET /api/apartados?estado=activo`):**
```json
[
  {"id": 5, "fecha": "2026-09-01", "cliente": "Carmen Ruiz", "telefono": "612 000 005", "email": "carmen@example.com", "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2026-11-30", "estado": "activo", "abonado": 49.9, "pendiente": 40.0},
  {"id": 7, "fecha": "2026-09-10", "cliente": "Jorge Martín", "telefono": "612 000 007", "email": "jorge@example.com", "producto": "Zapatilla running azul", "talla": "42", "precio": 64.5, "fecha_limite": "2026-12-09", "estado": "activo", "abonado": 39.0, "pendiente": 25.5},
  {"id": 9, "fecha": "2026-10-02", "cliente": "Lucía Gómez", "telefono": "612 000 009", "email": "lucia@example.com", "producto": "Sandalia tacón negra", "talla": "37", "precio": 45.0, "fecha_limite": "2026-12-31", "estado": "activo", "abonado": 33.0, "pendiente": 12.0}
]
```

**Todos los apartados (`GET /api/apartados`):**
```json
[
  {"id": 1, "fecha": "2026-10-02", "cliente": "Ana Torres", "producto": "Mocasín ante", "precio": 72.0, "fecha_limite": "2026-12-31", "estado": "activo", "abonado": 10.0, "pendiente": 62.0},
  {"id": 2, "fecha": "2026-10-10", "cliente": "Pedro Sanz", "producto": "Bota agua niño", "precio": 29.95, "fecha_limite": "2027-01-08", "estado": "activo", "abonado": 5.0, "pendiente": 24.95},
  {"id": 3, "fecha": "2026-09-15", "cliente": "Rosa Díaz", "producto": "Zapato vestir hombre", "precio": 95.0, "fecha_limite": "2026-12-14", "estado": "activo", "abonado": 20.0, "pendiente": 75.0},
  {"id": 4, "fecha": "2026-10-28", "cliente": "Miguel Ángel López", "producto": "Deportiva blanca", "precio": 55.0, "fecha_limite": "2027-01-26", "estado": "liquidado", "abonado": 55.0, "pendiente": 0.0},
  {"id": 5, "fecha": "2026-09-01", "cliente": "Carmen Ruiz", "producto": "Botín piel marrón", "precio": 89.9, "fecha_limite": "2026-11-30", "estado": "activo", "abonado": 49.9, "pendiente": 40.0},
  {"id": 6, "fecha": "2026-09-20", "cliente": "Sofía Navarro", "producto": "Bailarina roja", "precio": 39.9, "fecha_limite": "2026-12-19", "estado": "liquidado", "abonado": 39.9, "pendiente": 0.0}
]
```

**Vales (`GET /api/vales`):**
```json
[
  {"id": 1, "codigo": "VALE-001", "apartado_id": 8, "fecha": "2026-10-14", "importe": 30.0, "usado": 0},
  {"id": 2, "codigo": "VALE-002", "apartado_id": 9, "fecha": "2026-09-20", "importe": 15.0, "usado": 0}
]
```

**Detalle de liquidados (`GET /api/apartados/{id}`):**
- `GET /api/apartados/4`:
```json
{"id": 4, "fecha": "2026-10-28", "cliente": "Miguel Ángel López", "telefono": "612 000 004", "email": "miguel@example.com", "producto": "Deportiva blanca", "talla": "41", "precio": 55.0, "fecha_limite": "2027-01-26", "estado": "liquidado", "abonado": 55.0, "pendiente": 0.0, "abonos": [{"id": 401, "apartado_id": 4, "fecha": "2026-10-05", "importe": 20.0, "forma_pago": "efectivo"}, {"id": 402, "apartado_id": 4, "fecha": "2026-10-28", "importe": 35.0, "forma_pago": "tarjeta"}], "vale": null}
```
- `GET /api/apartados/6`:
```json
{"id": 6, "fecha": "2026-09-20", "cliente": "Sofía Navarro", "telefono": "612 000 006", "email": "sofia@example.com", "producto": "Bailarina roja", "talla": "36", "precio": 39.9, "fecha_limite": "2026-12-19", "estado": "liquidado", "abonado": 39.9, "pendiente": 0.0, "abonos": [{"id": 601, "apartado_id": 6, "fecha": "2026-09-22", "importe": 15.0, "forma_pago": "efectivo"}, {"id": 602, "apartado_id": 6, "fecha": "2026-10-18", "importe": 24.9, "forma_pago": "bizum"}], "vale": null}
```

**Resultado esperado (F-008-1):**
- `mes`: `2026-10` (octubre 2026).
- Recaudación ventas directas: `106,40 €` (`106.4`).
- Recaudación abonos: `45,00 €` (`45.0`).
- Recaudación total: `151,40 €` (`151.4`).
- Pendiente de cobro (suma de `pendiente` de activos): `77,50 €` (`77.5`).
- Apartados nuevos (por `fecha` en octubre): `3` (ids 1, 2, 4).
- Apartados liquidados (último abono en octubre): `2` (ids 4 y 6).
- Apartados vencidos (vales con `fecha` en octubre): `1` (VALE-001).
- Correo a `MARISA_EMAIL` con tabla HTML que contiene todos los valores anteriores. Asunto propuesto: `Informe mensual · octubre 2026` (texto literal pendiente de confirmar con Marisa, spec §11).
- No se incluyen datos personales de clientes en el correo.

## F-008-2 Mes sin datos + Always Output Data (CA-5, §7)

**Ventas:** `[]` (con `alwaysOutputData: true` n8n entrega `[{}]`).
**Abonos:** `[]`.
**Apartados activos:** `[]`.
**Todos los apartados:** `[]`.
**Vales:** `[]`.
**Detalle de liquidados:** ninguno (no hay liquidados).

**Resultado esperado (F-008-2):**
- El flujo no se detiene ni lanza error (los nodos HTTP Request con `alwaysOutputData: true` entregan `[{}]`).
- `mes`: `2026-10`.
- Recaudación ventas directas: `0,00 €` (`0`).
- Recaudación abonos: `0,00 €` (`0`).
- Recaudación total: `0,00 €` (`0`).
- Pendiente de cobro: `0,00 €` (`0`).
- Apartados nuevos: `0`.
- Apartados liquidados: `0`.
- Apartados vencidos: `0`.
- Correo a `MARISA_EMAIL` con las mismas secciones a cero y la nota «Sin movimientos en el mes».

## F-008-3 Liquidado aproximado por último abono (CA-3, §7)

**Ventas:** `[]`. **Abonos:** `[]`. **Apartados activos:** `[]`. **Vales:** `[]`.

**Todos los apartados (`GET /api/apartados`):**
```json
[
  {"id": 40, "fecha": "2026-09-01", "cliente": "Carmen Ruiz", "producto": "Botín piel marrón", "precio": 89.9, "fecha_limite": "2026-11-30", "estado": "liquidado", "abonado": 89.9, "pendiente": 0.0},
  {"id": 41, "fecha": "2026-09-05", "cliente": "Jorge Martín", "producto": "Zapatilla running azul", "precio": 64.5, "fecha_limite": "2026-12-04", "estado": "liquidado", "abonado": 64.5, "pendiente": 0.0},
  {"id": 42, "fecha": "2026-10-03", "cliente": "Lucía Gómez", "producto": "Sandalia tacón negra", "precio": 45.0, "fecha_limite": "2027-01-01", "estado": "liquidado", "abonado": 45.0, "pendiente": 0.0},
  {"id": 43, "fecha": "2026-10-10", "cliente": "Ana Torres", "producto": "Mocasín ante", "precio": 72.0, "fecha_limite": "2027-01-08", "estado": "liquidado", "abonado": 72.0, "pendiente": 0.0}
]
```

**Detalle de liquidados:**
- `GET /api/apartados/40` (último abono en octubre → cuenta):
```json
{"id": 40, "fecha": "2026-09-01", "cliente": "Carmen Ruiz", "telefono": "612 000 040", "email": "carmen@example.com", "producto": "Botín piel marrón", "talla": "38", "precio": 89.9, "fecha_limite": "2026-11-30", "estado": "liquidado", "abonado": 89.9, "pendiente": 0.0, "abonos": [{"id": 4001, "apartado_id": 40, "fecha": "2026-09-20", "importe": 30.0, "forma_pago": "efectivo"}, {"id": 4002, "apartado_id": 40, "fecha": "2026-10-15", "importe": 59.9, "forma_pago": "tarjeta"}], "vale": null}
```
- `GET /api/apartados/41` (último abono en septiembre → no cuenta):
```json
{"id": 41, "fecha": "2026-09-05", "cliente": "Jorge Martín", "telefono": "612 000 041", "email": "jorge@example.com", "producto": "Zapatilla running azul", "talla": "42", "precio": 64.5, "fecha_limite": "2026-12-04", "estado": "liquidado", "abonado": 64.5, "pendiente": 0.0, "abonos": [{"id": 4101, "apartado_id": 41, "fecha": "2026-09-10", "importe": 20.0, "forma_pago": "efectivo"}, {"id": 4102, "apartado_id": 41, "fecha": "2026-09-28", "importe": 44.5, "forma_pago": "bizum"}], "vale": null}
```
- `GET /api/apartados/42` (sin abonos → no cuenta, no se puede aproximar):
```json
{"id": 42, "fecha": "2026-10-03", "cliente": "Lucía Gómez", "telefono": "612 000 042", "email": "lucia@example.com", "producto": "Sandalia tacón negra", "talla": "37", "precio": 45.0, "fecha_limite": "2027-01-01", "estado": "liquidado", "abonado": 45.0, "pendiente": 0.0, "abonos": [], "vale": null}
```
- `GET /api/apartados/43` → `404` con `{"detail": "Apartado no encontrado"}` (detalle inaccesible).

**Resultado esperado (F-008-3):**
- Apartados liquidados del mes: `1` (solo id 40).
- id 41 no cuenta (último abono en septiembre).
- id 42 no cuenta (sin abonos, no se puede aproximar la fecha de liquidación).
- id 43: se avisa a Marisa con el motivo (`detail` del 404) y se continúa; el conteo de liquidados puede quedar incompleto (aproximación documentada, spec §7).
- El informe se envía igualmente (con los datos disponibles).

## F-008-4 Vencido por vale (CA-3, §7)

**Ventas:** `[]`. **Abonos:** `[]`. **Apartados activos:** `[]`. **Todos los apartados:** `[]` (el conteo de vencidos se basa en vales, no en apartados).

**Vales (`GET /api/vales`):**
```json
[
  {"id": 1, "codigo": "VALE-101", "apartado_id": 50, "fecha": "2026-10-03", "importe": 25.0, "usado": 0},
  {"id": 2, "codigo": "VALE-102", "apartado_id": 51, "fecha": "2026-10-31", "importe": 10.0, "usado": 0},
  {"id": 3, "codigo": "VALE-103", "apartado_id": 52, "fecha": "2026-09-30", "importe": 15.0, "usado": 0},
  {"id": 4, "codigo": "VALE-104", "apartado_id": 53, "fecha": "2026-11-01", "importe": 5.0, "usado": 0}
]
```

**Resultado esperado (F-008-4):**
- Apartados vencidos del mes: `2` (VALE-101 del 2026-10-03 y VALE-102 del 2026-10-31; límites incluidos).
- VALE-103 (2026-09-30) no cuenta (septiembre).
- VALE-104 (2026-11-01) no cuenta (noviembre).
- Un vale por apartado como mucho; no se duplican.

## F-008-5 Pendiente de activos (CA-2, CA-4)

**Ventas:** `[]`. **Abonos:** `[]`. **Todos los apartados:** `[]`. **Vales:** `[]`.

**Apartados activos (`GET /api/apartados?estado=activo`):**
```json
[
  {"id": 60, "fecha": "2026-09-01", "cliente": "Carmen Ruiz", "producto": "Botín piel marrón", "precio": 89.9, "fecha_limite": "2026-11-30", "estado": "activo", "abonado": 79.9, "pendiente": 0.1},
  {"id": 61, "fecha": "2026-09-10", "cliente": "Jorge Martín", "producto": "Zapatilla running azul", "precio": 64.5, "fecha_limite": "2026-12-09", "estado": "activo", "abonado": 44.3, "pendiente": 0.2},
  {"id": 62, "fecha": "2026-10-02", "cliente": "Lucía Gómez", "producto": "Sandalia tacón negra", "precio": 45.0, "fecha_limite": "2026-12-31", "estado": "activo", "abonado": 0.0, "pendiente": 100.0}
]
```

**Resultado esperado (F-008-5):**
- Pendiente de cobro: `100,30 €` (`100.3`) = `0.1 + 0.2 + 100.0`, redondeado a 2 decimales.
- Los sumandos (`0.1`, `0.2`, `100.0`) no se alteran.
- Recaudación ventas/abonos: `0,00 €`. Nuevos/liquidados/vencidos: `0`.

## F-008-6 Redondeo de totales (CA-4, §7)

**Ventas (`GET /api/ventas?desde=2026-10-01&hasta=2026-10-31`):**
```json
[
  {"id": 1, "fecha": "2026-10-05", "concepto": "Cordones", "importe": 0.1, "forma_pago": "efectivo"},
  {"id": 2, "fecha": "2026-10-12", "concepto": "Bolsita", "importe": 0.2, "forma_pago": "efectivo"}
]
```

**Abonos (`GET /api/abonos?desde=2026-10-01&hasta=2026-10-31`):**
```json
[
  {"id": 10, "apartado_id": 5, "fecha": "2026-10-08", "importe": 0.1, "forma_pago": "efectivo"},
  {"id": 11, "apartado_id": 7, "fecha": "2026-10-15", "importe": 0.2, "forma_pago": "efectivo"}
]
```

**Apartados activos:** `[]`. **Todos los apartados:** `[]`. **Vales:** `[]`.

**Resultado esperado (F-008-6):**
- Recaudación ventas directas: `0,30 €` (`0.3`), nunca `0.30000000000000004`.
- Recaudación abonos: `0,30 €` (`0.3`).
- Recaudación total: `0,60 €` (`0.6`).
- Los sumandos individuales (`0.1`, `0.2`) no se alteran.
- Solo los totales se redondean a 2 decimales.

## F-008-7 Nuevos por fecha del apartado, no por abonos (CA-3, §7)

**Ventas:** `[]`. **Vales:** `[]`. **Apartados activos:** `[]`.

**Abonos (`GET /api/abonos?desde=2026-10-01&hasta=2026-10-31`):**
```json
[
  {"id": 301, "apartado_id": 70, "fecha": "2026-10-20", "importe": 10.0, "forma_pago": "efectivo"}
]
```

**Todos los apartados (`GET /api/apartados`):**
```json
[
  {"id": 70, "fecha": "2026-09-15", "cliente": "Rosa Díaz", "producto": "Zapato vestir hombre", "precio": 95.0, "fecha_limite": "2026-12-14", "estado": "activo", "abonado": 30.0, "pendiente": 65.0},
  {"id": 71, "fecha": "2026-10-05", "cliente": "Pedro Sanz", "producto": "Bota agua niño", "precio": 29.95, "fecha_limite": "2027-01-03", "estado": "activo", "abonado": 5.0, "pendiente": 24.95}
]
```

**Resultado esperado (F-008-7):**
- Apartados nuevos: `1` (solo id 71, con `fecha` en octubre).
- id 70 NO cuenta como nuevo aunque tenga un abono en octubre (su `fecha` es de septiembre).
- Recaudación abonos: `10,00 €` (el abono de id 70 sí cuenta para la recaudación).
- Demuestra que «nuevos» se cuentan por `fecha` del apartado, no por abonos.

## F-008-8 Zona horaria `Europe/Madrid` (§7)

Prueba de configuración del nodo `Calcular mes anterior` (Code), no de payloads de la API.

- Configurar `ZONA_HORARIA = Europe/Madrid`.
- Simular «hoy» = `2026-10-01 00:30 UTC` (equivale a `2026-09-30 22:30 Europe/Madrid`).
- **Resultado esperado:** `desde = 2026-08-01`, `hasta = 2026-08-31`, `mes = 2026-08` (mes anterior en Madrid = agosto 2026), NO septiembre 2026 (que sería el resultado si se calculara en UTC).
- Con `ZONA_HORARIA = UTC` el mismo «hoy» daría `desde = 2026-09-01`, `hasta = 2026-09-30` (contraste que evidencia el uso de `Europe/Madrid`).
- Los movimientos de agosto 2026 se contarían; los de septiembre 2026 no.

## F-008-9 Timeout / API no responde (§7)

- Desconectar la tienda o apuntar un nodo HTTP Request a un host inalcanzable (`http://tienda:8000` sin servicio).
- **Resultado esperado:** Retry On Fail con 2 intentos (`maxTries: 2`, espera 3 s entre intentos); si persiste, se ejecuta el Error Workflow `[ERR] Avisos de error` (`005`) con flujo `[008] Informe mensual`, nodo afectado y mensaje de error. No se envía el informe (o se envía parcial si el error es en un nodo no crítico y `On Error → Continue` lo permite).

## F-008-10 Error 401 clave inválida (§7)

- Llamar a cualquier endpoint con una credencial `PF · API tienda` cuyo `X-API-Key` sea inválido.
- **Resultado esperado:** error de configuración; aviso inmediato por el Error Workflow, sin reintentar en bucle. No se reintenta indefinidamente.

## F-008-11 Error 404 recurso inexistente (§7)

- `GET /api/apartados/999999` (apartado que no existe) desde el nodo `Pedir detalle de liquidados`.
- **Resultado esperado:** aviso a Marisa con el `detail` del error (`{"detail": "..."}`); el flujo continúa con el resto del informe si es posible. El conteo de liquidados puede quedar incompleto (aproximación documentada).

## F-008-12 Error 422 regla de negocio (§7)

- Provocar un `422` (por ejemplo, parámetros inválidos en la consulta) tratado con `On Error → Continue (using error output)`.
- **Resultado esperado:** el flujo no se rompe; se avisa a Marisa con el `detail` del error; se continúa con el resto del informe si es posible.

## F-008-13 Reejecución el mismo día (§7)

- Ejecutar el flujo dos veces el mismo día 1 (manual o reprogramado).
- **Resultado esperado:** se envía otro correo (no hay idempotencia estricta, FL-07 no está en la lista de flujos idempotentes). No se guardan filas en ningún histórico (no hay Google Sheets), por lo que no se duplican filas; solo se duplica el envío del email.

## F-008-14 Error de Gmail al enviar (§7)

- Configurar `MARISA_EMAIL` a una dirección inválida o revocar la credencial `PF · Gmail` para que el envío falle.
- **Resultado esperado:** reintento con espera (`retryOnFail`, `maxTries: 2`); si persiste, se ejecuta el Error Workflow `[ERR] Avisos de error`. No se envía ningún otro correo.

## Cómo probar

1. Abrir `[008] Informe mensual` en el editor y fijar (*Pin Data*) en cada nodo HTTP Request la respuesta JSON del caso (un array; para listas vacías usar `[]` y activar `alwaysOutputData: true`).
2. Para los detalles de liquidados, fijar la respuesta de `Pedir detalle de liquidados` por item o simular el `404`/`422` con *On Error → Continue*.
3. *Test workflow* y comprobar en el nodo `Sumar informe` los valores calculados y en `Enviar informe a Marisa` el asunto/cuerpo contra los esperados.
4. Para no escribir a nadie, desactivar el nodo Gmail y revisar su entrada, o apuntar `MARISA_EMAIL` a un buzón de pruebas `@example.com`.
5. **Quitar el pin data antes de exportar** el JSON.

Pruebas de extremo a extremo con los datos de ejemplo de la app (`backend/seed.py`): los ids, nombres y fechas cambian con el día de arranque, así que los totales esperados se recalculan sumando las respuestas reales de `GET /api/ventas`, `GET /api/abonos`, `GET /api/apartados` y `GET /api/vales` para el mes anterior. Reiniciar los datos de ejemplo: `docker compose down -v && docker compose up -d`.

## Cobertura

- CA-1 (RF-37) → F-008-1, F-008-6.
- CA-2 (RF-38) → F-008-1, F-008-5.
- CA-3 (RF-39) → F-008-1, F-008-3, F-008-4, F-008-7.
- CA-4 (RF-40) → F-008-1, F-008-5, F-008-6.
- CA-5 (RF-41) → F-008-2.
- Mes sin datos / lista vacía / Always Output Data (§7) → F-008-2.
- API no responde / timeout (§7) → F-008-9.
- Error 401 (§7) → F-008-10.
- Error 404 (§7) → F-008-3 (detalle inaccesible), F-008-11.
- Error 422 (§7) → F-008-12.
- Reejecución el mismo día (§7) → F-008-13.
- Apartado liquidado sin abonos o detalle inaccesible (§7) → F-008-3.
- Apartado con fecha fuera del mes pero abono en el mes (§7) → F-008-7.
- Vales con fecha en el mes (§7) → F-008-4.
- Redondeo (§7) → F-008-5, F-008-6.
- Zona horaria (§7) → F-008-8.
- Error de Gmail al enviar (§7) → F-008-14.
- Datos personales (§9): ningún caso incluye `cliente`/`telefono`/`email` en el correo esperado; el flujo solo agrega conteos e importes.
