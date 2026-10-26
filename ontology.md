# SCOPE: infraestructura-agentes (NO tocar backend/frontend/workflows)

# Ontología del dominio · Zapatería Paso Firme

Modelo conceptual para que un agente entienda el negocio **sin leer todo el código**.
Fuente de verdad, por orden: `backend/database.py` (esquema) → `backend/models/*.py` (reglas) → `backend/config.py` (constantes) → `docs/guia-de-la-app.md`.
Si este documento y el código no coinciden, **manda el código** y hay que actualizar este archivo.

Leyenda de propiedad:
- **[APP]**: lo guarda y lo calcula la app. n8n lo lee, nunca lo recalcula.
- **[N8N]**: no existe en la app; lo produce o guarda n8n (Google Sheets, correo…).
- **[EXT]**: viene de fuera (banco, cliente, Telegram).

---

## 1. Actores

| Actor | Rol | Canal |
|---|---|---|
| **Marisa** | Dueña. Recibe cierres, informes, avisos de error y preguntas sobre pagos dudosos. Única usuaria autorizada para consultas de negocio (HU-12) | `<<PENDIENTE: correo o Telegram de la tienda>>` |
| **Dependienta** | Registra apartados, abonos y ventas en la app | App web (`frontend/`) |
| **Cliente** | Aparta zapatos, paga abonos, recibe confirmaciones, recibos, recordatorios y vales | Correo (`email`) o teléfono (`telefono`) del apartado |
| **Banco** | Envía avisos de Bizum o transferencia por correo | `data/correos/*.eml` (ejemplos) |
| **n8n** | Orquestador: reacciona a eventos, consulta y actúa sobre la API, notifica | Webhook + API REST |

---

## 2. Entidades

### 2.1 Apartado [APP] · tabla `apartados`

Reserva de **un solo par** (producto + talla) que el cliente paga a plazos.

| Atributo | Tipo | Notas |
|---|---|---|
| `id` | entero | Nº de apartado. Los clientes lo citan en el concepto («apartado 2») |
| `fecha` | fecha `AAAA-MM-DD` | Día de alta. Solo se fija a mano al migrar datos antiguos |
| `cliente` | texto | Nombre libre. **No hay entidad Cliente**: ver 2.6 |
| `telefono` | texto, opcional | Formato libre («612 345 001» o «612345001») |
| `email` | texto, opcional | Puede faltar: los flujos deben avisar a la tienda en vez de fallar |
| `producto` | texto | Modelo, en texto libre. No hay catálogo |
| `talla` | texto, opcional | |
| `precio` | decimal > 0 | |
| `fecha_limite` | fecha | **Calculada** al crear: `fecha + 90 días` |
| `estado` | enum `EstadoApartado` | `activo` (por defecto), `liquidado`, `vencido` |
| `abonado` | decimal | **Derivado** (no está en la tabla): suma de sus abonos, redondeada a 2 decimales |
| `pendiente` | decimal | **Derivado**: `precio − abonado` |

### 2.2 Abono [APP] · tabla `abonos`

Pago parcial de un apartado. El abono inicial también es un abono (se crea a la vez que el apartado).

| Atributo | Tipo | Notas |
|---|---|---|
| `id` | entero | |
| `apartado_id` | entero → Apartado | |
| `fecha` | fecha | Por defecto hoy |
| `importe` | decimal > 0 | |
| `forma_pago` | enum `FormaPago` | |

### 2.3 Venta [APP] · tabla `ventas`

Venta directa de mostrador, **sin apartado**.

| Atributo | Tipo | Notas |
|---|---|---|
| `id`, `fecha`, `concepto` (texto), `importe` (decimal > 0), `forma_pago` (`FormaPago`) | | |

### 2.4 Vale [APP] · tabla `vales`

Crédito de compra que recibe el cliente cuando su apartado **vence**. Lo abonado no se devuelve en efectivo.

| Atributo | Tipo | Notas |
|---|---|---|
| `id` | entero | |
| `codigo` | texto único | Formato `VALE-00016` (id del apartado con 5 dígitos) |
| `apartado_id` | entero → Apartado | Como mucho un vale por apartado |
| `fecha` | fecha | Día en que se venció |
| `importe` | decimal | = `abonado` del apartado en el momento de vencer |
| `usado` | 0/1 | Existe en la tabla, pero **la API no tiene endpoint para marcarlo como usado** |

### 2.5 Evento [APP → N8N]

Aviso que la app envía al webhook de n8n: `{"evento": <TipoEvento>, "datos": {...}}`. Se envía después de responder, una sola vez y **sin reintentos**.

| `TipoEvento` | Cuándo | `datos` |
|---|---|---|
| `apartado.creado` | Alta de apartado | Apartado (con `abonado`, `pendiente`, `estado`) |
| `abono.registrado` | Abono nuevo | Apartado actualizado **+ `importe`** del abono. Ojo: `id` es el del **apartado**; no trae `forma_pago` ni id del abono |
| `venta.registrada` | Venta directa | Venta |
| `apartado.vencido` | `POST /vencer` correcto | `{ "apartado": {...}, "vale": {...} }` |

### 2.6 Cliente (concepto, no entidad) [APP, implícito]

La app **no tiene tabla de clientes**. Un «cliente» es el trío `cliente` + `telefono` + `email` repetido en cada apartado.
Consecuencias para los flujos:
- Identificar a alguien por nombre es **ambiguo** (nombres abreviados, mayúsculas, varios apartados de la misma persona).
- La búsqueda de la API (`GET /api/apartados?q=`) usa coincidencia parcial sobre cliente, producto, teléfono o nº.
- El consentimiento para recibir mensajes (HU-14) **no existe en la app**: `<<PENDIENTE: decidir dónde se guarda (n8n / Google Sheets)>>`.

### 2.7 Producto (concepto, no entidad)

Texto libre `producto` + `talla` dentro del apartado o `concepto` en la venta. **No existe catálogo, stock ni inventario.**
«Volver a la venta» tras un vencimiento es una acción física de la tienda que n8n solo comunica.

### 2.8 Entidades que produce n8n [N8N]

| Entidad | Qué es | Dónde se guarda |
|---|---|---|
| **CierreDiario** | Totales del día por forma de pago (ventas, abonos, total) | `<<PENDIENTE: Google Sheets u otra herramienta>>` |
| **InformeMensual** | Recaudación del mes (ventas y abonos por separado), pendiente total, apartados nuevos/liquidados/vencidos | Correo a Marisa (PDF o tabla) |
| **Recordatorio** | Aviso al cliente a 7 y 1 días de `fecha_limite` | Registro para no repetir: `<<PENDIENTE>>` |
| **Notificacion** | Mensaje enviado (cliente o tienda) | Canal elegido |
| **ConsultaPendiente** | Pago dudoso que Marisa debe resolver | Correo/Telegram a Marisa |
| **AvisoBancario** [EXT] | Correo del banco: ordenante, importe, concepto (o publicidad) | Bandeja de entrada leída por n8n |

---

## 3. Enumeraciones

| Enum | Valores | Fuente |
|---|---|---|
| `EstadoApartado` | `activo`, `liquidado`, `vencido` | `CHECK` en `backend/database.py` |
| `FormaPago` | `efectivo`, `tarjeta`, `bizum` | `FORMAS_PAGO` en `backend/config.py` |
| `TipoEvento` | `apartado.creado`, `abono.registrado`, `venta.registrada`, `apartado.vencido` | `backend/controllers/*.py` |

> ⚠️ Una **transferencia** bancaria no es una `FormaPago` válida. Cómo registrarla es una decisión abierta: `<<PENDIENTE: ¿se registra como bizum?, ¿se pide a la profe ampliar la app?>>`.

---

## 4. Relaciones

```
Cliente (implícito) 1 ──── * Apartado 1 ──── 1..* Abono
                                  │
                                  └──── 0..1 Vale        (solo si estado = vencido)

Venta (independiente; sin cliente ni apartado)

Evento ──referencia──▶ Apartado | Venta | (Apartado + Vale)
AvisoBancario ──(n8n lo resuelve)──▶ 0..1 Apartado ──▶ Abono nuevo | ConsultaPendiente
CierreDiario  ──agrega──▶ Ventas + Abonos de un día
InformeMensual ──agrega──▶ Ventas + Abonos de un mes + Apartados activos (pendiente)
```

---

## 5. Ciclo de vida del apartado

```
            alta (abono inicial ≥ 5 € y ≤ precio)
                         │
                         ▼
 ┌─────────────┐  abono deja pendiente = 0 (lo hace la app)   ┌─────────────┐
 │   activo    │ ───────────────────────────────────────────▶ │  liquidado  │  final
 └─────────────┘                                              └─────────────┘
        │  POST /api/apartados/{id}/vencer  (lo llama n8n; solo si hoy > fecha_limite)
        ▼
 ┌─────────────┐
 │   vencido   │  final · genera Vale con importe = abonado
 └─────────────┘
```

Si el abono inicial es igual al precio, el apartado nace directamente `liquidado`.
Un apartado con el plazo pasado **sigue `activo`** hasta que alguien lo vence.

---

## 6. Reglas de negocio (con su origen en el código)

| ID | Regla | Dónde se aplica | Error |
|---|---|---|---|
| R-01 | Abono inicial ≥ `ABONO_MINIMO` (5 €) | `models/apartado.py · crear` | 422 |
| R-02 | Abono inicial ≤ precio | `models/apartado.py · crear` | 422 |
| R-03 | Precio > 0 | `models/apartado.py · crear` y schema | 422 |
| R-04 | `fecha_limite = fecha + PLAZO_DIAS` (90) | `models/apartado.py · crear` | — |
| R-05 | Solo se abona un apartado `activo` | `models/abono.py · registrar` | 422 |
| R-06 | No se abona si la fecha del abono es posterior a `fecha_limite` (el mismo día sí se puede) | `models/abono.py · registrar` | 422 |
| R-07 | Importe del abono > 0 y ≤ `pendiente` | `models/abono.py · registrar` | 422 |
| R-08 | `forma_pago` ∈ `FormaPago` | modelos de apartado, abono y venta | 422 |
| R-09 | Si `pendiente` llega a 0 → `liquidado` automáticamente | `models/abono.py`, `models/apartado.py` | — |
| R-10 | Vencer solo un `activo` y solo si hoy > `fecha_limite` | `models/apartado.py · vencer` | 422 |
| R-11 | Al vencer se crea un Vale `VALE-NNNNN` con importe = `abonado` | `models/apartado.py · vencer` | — |
| R-12 | Un apartado = un par (un producto + una talla) | Enunciado; la app guarda un solo `producto` | — |
| R-13 | Importe de venta > 0 | `models/venta.py` | 422 |

## 7. Métricas de negocio (las calcula n8n agregando datos de la app)

| Métrica | Definición | Datos de la API |
|---|---|---|
| Ventas del día | Ventas directas + abonos cobrados ese día (los iniciales cuentan), por forma de pago | `GET /api/ventas?desde=D&hasta=D` + `GET /api/abonos?desde=D&hasta=D` |
| Recaudación mensual | Todo lo cobrado en el mes, separando ventas y abonos | Igual, con el rango del mes |
| Total pendiente de cobro | Suma de `pendiente` de los apartados `activo` | `GET /api/apartados?estado=activo` |
| Apartados por estado | Conteo | `GET /api/apartados/resumen` |

Sumar movimientos (ventas, abonos) es trabajo de n8n. Recalcular `abonado`/`pendiente` de un apartado **no**: esos valores los da la app.

## 8. Glosario

| Término | Significado |
|---|---|
| Apartar | Reservar unos zapatos dejando un abono inicial |
| Abono | Pago parcial de un apartado |
| Liquidar | Terminar de pagar un apartado |
| Vencer | Cerrar un apartado fuera de plazo; los zapatos vuelven a la venta y lo abonado pasa a vale |
| Vale | Crédito de compra para el cliente |
| Cierre de caja | Resumen diario de lo cobrado |
| Ordenante | Quien envía el Bizum o la transferencia |
| Concepto | Texto libre que escribe el ordenante (a veces trae el nº de apartado) |
